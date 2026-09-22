"""KB Supervisor Agent - Main CLI entry point."""

import argparse
import logging
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

from .config import Settings, ensure_directories, load_config
from .utils.qwen_interface import QwenInterface
from .utils.trace_loader import TraceLoader
from .utils.trace_analyzer import TraceAnalyzer
from .utils.gap_identifier import GapIdentifier
from .utils.report_generator import ReportGenerator
from .utils.skill_pipeline_bridge import SkillPipelineBridge
from .utils.gap_classifier import (
    GapClassifier,
    OUT_OF_SCOPE_GENERAL,
    NOISE,
    OUT_OF_SCOPE_PRICING,
    OUT_OF_SCOPE_ACCOUNT_SUPPORT,
)
from .utils.hermes_judge import HermesJudge, is_hermes_available
from .utils.hermes_coordinator import HermesCoordinator
from .utils.kanban_writer import KanbanWriter


def setup_logging(logs_dir: Path, timestamp: str) -> logging.Logger:
    """Set up structured logging to file and console.

    Args:
        logs_dir: Directory to write logs.
        timestamp: Timestamp string for log filename.

    Returns:
        Configured logger instance.
    """
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / f"supervisor_{timestamp}.log"

    # Console handler (INFO level)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(console_formatter)

    # File handler (DEBUG level)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s:%(funcName)s:%(lineno)d: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)

    # Root logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logging.getLogger(__name__)


def main() -> int:
    """Main entry point for supervisor agent.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="KB Supervisor - On-demand KB gap analysis and recommendations"
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate analysis report",
    )
    parser.add_argument(
        "--max-gaps",
        type=int,
        default=20,
        help="Maximum number of gaps to report (default: 20)",
    )
    parser.add_argument(
        "--min-severity",
        type=float,
        default=0.0,
        help="Minimum severity score to include (default: 0.0)",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=14,
        help="Only analyze traces from the last N days (default: 14). "
             "Use 0 to analyze all traces.",
    )

    args = parser.parse_args()

    if not args.report:
        parser.print_help()
        return 0

    # Load configuration
    try:
        config = load_config()
    except Exception as e:
        print(f"Failed to load configuration: {e}")
        return 1

    # Set up logging
    IST = timezone(timedelta(hours=5, minutes=30))
    timestamp = datetime.now(IST).strftime("%Y%m%d_%H%M%S")
    logger = setup_logging(config.logs_dir, timestamp)

    logger.info("=" * 80)
    logger.info("KB Supervisor Agent Starting")
    logger.info(f"Timestamp: {timestamp}")
    days_label = f"last {args.days} days" if args.days > 0 else "all time"
    logger.info(f"Config: max_gaps={args.max_gaps}, min_severity={args.min_severity}, window={days_label}")
    logger.info("=" * 80)

    try:
        # Ensure directories exist
        ensure_directories(config)

        # Step 1: Load and update traces
        logger.info("STEP 1: Loading traces from cache and fetching new traces")
        trace_loader = TraceLoader(
            cache_path=config.cache_dir / "langfuse_traces_cache.json",
            langfuse_public_key=config.langfuse_public_key,
            langfuse_secret_key=config.langfuse_secret_key,
            langfuse_host=config.langfuse_host,
        )

        cache = trace_loader.load_cache()
        last_timestamp = trace_loader.get_last_timestamp()
        logger.info(f"Cache loaded: {len(cache.get('traces', []))} traces")

        new_traces = trace_loader.fetch_new_traces(last_timestamp)
        trace_loader.append_to_cache(new_traces)
        all_traces = trace_loader.get_all_traces()
        logger.info(f"Total traces in cache: {len(all_traces)}")

        # Filter to recent window so fixed gaps don't keep reappearing
        if args.days > 0:
            cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
            filtered = []
            for t in all_traces:
                ts_str = t.get("timestamp") or t.get("createdAt") or ""
                try:
                    ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                    if ts >= cutoff:
                        filtered.append(t)
                except (ValueError, AttributeError):
                    filtered.append(t)  # keep traces with unparseable timestamps
            logger.info(
                f"Recency filter: keeping {len(filtered)}/{len(all_traces)} traces "
                f"from last {args.days} days (since {cutoff.strftime('%Y-%m-%d')})"
            )
            all_traces = filtered

        if not all_traces:
            logger.warning("No traces found in window. Exiting.")
            return 0

        # Step 2: Analyze traces
        logger.info("STEP 2: Analyzing traces")
        analyzer = TraceAnalyzer()
        gaps = analyzer.analyze(all_traces)
        logger.info(f"Identified {len(gaps)} gaps")

        # Step 3: Identify top gaps
        logger.info("STEP 3: Identifying top gaps by severity")
        identifier = GapIdentifier()
        selected_gaps = identifier.identify(
            gaps,
            max_gaps=args.max_gaps,
            min_severity=args.min_severity,
        )
        logger.info(f"Selected {len(selected_gaps)} gaps for detailed analysis")

        # Step 3.5: Classify each gap against the REAL skill pipeline (NEW)
        #
        # Replaces the old kb_searcher/rag_diagnostician keyword-scoring
        # diagnosis (which produced a uniform, miscalibrated "RETRIEVAL 85%"
        # verdict on every gap). GapClassifier re-runs each gap's failure
        # queries through the actual skill/kb_answer.py pipeline (via
        # SkillPipelineBridge) and classifies by what really happened:
        # ALREADY_FIXED, CODE_GAP_ALIAS_CANDIDATE, CODE_GAP_MISSING_CONCEPT,
        # CODE_GAP_NEEDS_INVESTIGATION, CONTENT_GAP, OUT_OF_SCOPE_PRICING,
        # OUT_OF_SCOPE_ACCOUNT_SUPPORT, or MIXED (heterogeneous gap).
        logger.info("STEP 3.5: Classifying gaps against the real skill pipeline")
        bridge = SkillPipelineBridge()
        classifier = GapClassifier(bridge)

        classifications = {}
        for i, gap in enumerate(selected_gaps, 1):
            gap_key = f"Gap #{i}"
            logger.info(f"  Classifying {gap.module}/{gap.intent}...")
            result = classifier.classify_gap(gap.failure_examples, max_samples=10)
            classifications[gap_key] = result
            logger.info(f"    {gap_key}: {result['category']} (confidence={result['confidence']})")

        hermes_available = is_hermes_available()
        judge = HermesJudge(bridge=bridge) if hermes_available else None
        logger.info(f"STEP 3.6: Hermes availability: {hermes_available} — skipping single-shot judge, routing all gaps to coordinator")

        # Step 3.65 — 4-bucket classification via multi-agent Hermes coordinator.
        # Each gap gets its own worker running a 3-turn conversation:
        #   Turn 1: deep analysis (pipeline signal, KB inventory, all queries)
        #   Turn 2: adversarial self-challenge (checks FALSE-POSITIVE flags, ANSWERED queries)
        #   Turn 3: final verdict → writes JSON, posts to kanban
        # Workers run in parallel (up to 8 concurrent Hermes calls).
        # Gaps already flagged as out-of-scope/noise by the deterministic classifier
        # are skipped to avoid wasting Hermes turns.
        logger.info("STEP 3.65: Running 4-bucket classification via Hermes coordinator")

        # Fast-path: short-circuit deterministic out-of-scope/noise gaps before Hermes
        coordinator_gaps = []
        coordinator_classifications = {}
        four_bucket_verdicts = {}

        for idx, gap in enumerate(selected_gaps):
            gap_key = f"{gap.module}/{gap.intent}"
            old_key = f"Gap #{idx + 1}"
            cat = classifications.get(old_key, {}).get("category", "")
            if cat in (OUT_OF_SCOPE_PRICING, OUT_OF_SCOPE_ACCOUNT_SUPPORT, OUT_OF_SCOPE_GENERAL, NOISE):
                four_bucket_verdicts[gap_key] = {
                    "bucket": "OUT_OF_SCOPE",
                    "confidence": "high",
                    "reasoning": cat,
                    "keywords_to_add": [],
                    "doc_to_create": None,
                    "doc_outline": None,
                    "matching_doc": None,
                    "root_cause": None,
                    "doc_priority": None,
                    "reason_ignored": cat,
                }
                logger.info(f"  4-bucket: {gap_key} → OUT_OF_SCOPE (deterministic: {cat})")
            else:
                coordinator_gaps.append(gap)
                coordinator_classifications[f"Gap #{len(coordinator_gaps)}"] = classifications.get(old_key, {})

        if coordinator_gaps:
            if hermes_available:
                kanban = KanbanWriter()
                coordinator = HermesCoordinator(judge=judge, kanban=kanban)
                coord_verdicts = coordinator.run(
                    gaps=coordinator_gaps,
                    classifications=coordinator_classifications,
                    all_traces=all_traces,
                    max_workers=min(len(coordinator_gaps), 8),
                )
                four_bucket_verdicts.update(coord_verdicts)
                for gap_key, verdict in coord_verdicts.items():
                    logger.info(f"  4-bucket: {gap_key} → {verdict.get('bucket')} ({verdict.get('confidence')})")
            else:
                for gap in coordinator_gaps:
                    gap_key = f"{gap.module}/{gap.intent}"
                    four_bucket_verdicts[gap_key] = {
                        "bucket": "HAS_DOCS_FAILS", "confidence": "low",
                        "reasoning": "Hermes not available — degraded", "degraded": True,
                        "keywords_to_add": [], "doc_to_create": None,
                        "doc_outline": None, "matching_doc": None,
                        "root_cause": None, "doc_priority": None, "reason_ignored": None,
                    }

        # Step 4: Generate report
        logger.info("STEP 4: Generating report with gap classifications")
        qwen = QwenInterface(
            base_url=config.anthropic_base_url,
            auth_token=config.anthropic_auth_token,
            model=config.anthropic_model,
            temperature=config.anthropic_temperature,
            max_tokens=config.anthropic_max_tokens,
            timeout_seconds=config.qwen_timeout_seconds,
        )

        generator = ReportGenerator(qwen)
        report_path = config.reports_dir / f"supervisor_{timestamp}.md"
        report_text = generator.generate_report(
            selected_gaps,
            all_traces,
            report_path,
            classifications=classifications,
            judge_verdicts=four_bucket_verdicts,
            trace_window_days=args.days,
        )

        logger.info("=" * 80)
        logger.info("KB Supervisor Agent Completed Successfully")
        logger.info(f"Report: {report_path}")
        logger.info(f"Logs: {config.logs_dir / f'supervisor_{timestamp}.log'}")
        logger.info("=" * 80)

        # Print summary to console
        print("\n" + "=" * 80)
        print("SUPERVISOR REPORT GENERATED")
        print("=" * 80)
        print(f"✓ Traces analyzed: {len(all_traces)}")
        print(f"✓ New traces: {len(new_traces)}")
        print(f"✓ Gaps identified: {len(selected_gaps)}")
        print(f"✓ Report: {report_path}")
        print(f"✓ Logs: {config.logs_dir / f'supervisor_{timestamp}.log'}")
        print("=" * 80 + "\n")

        return 0

    except Exception as e:
        logger.exception(f"Supervisor agent failed: {e}")
        print(f"\n✗ Supervisor agent failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
