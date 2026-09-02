"""KB Supervisor Agent - Main CLI entry point."""

import argparse
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

from .config import Settings, ensure_directories, load_config
from .utils.qwen_interface import QwenInterface
from .utils.trace_loader import TraceLoader
from .utils.trace_analyzer import TraceAnalyzer
from .utils.gap_identifier import GapIdentifier
from .utils.report_generator import ReportGenerator
from .utils.skill_pipeline_bridge import SkillPipelineBridge
from .utils.gap_classifier import GapClassifier, ALREADY_FIXED, CODE_GAP_NEEDS_INVESTIGATION
from .utils.hermes_judge import HermesJudge, is_hermes_available
from .utils.proposals_writer import ProposalsWriter


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
        default=10,
        help="Maximum number of gaps to report (default: 10)",
    )
    parser.add_argument(
        "--min-severity",
        type=float,
        default=0.0,
        help="Minimum severity score to include (default: 0.0)",
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
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    logger = setup_logging(config.logs_dir, timestamp)

    logger.info("=" * 80)
    logger.info("KB Supervisor Agent Starting")
    logger.info(f"Timestamp: {timestamp}")
    logger.info(f"Config: max_gaps={args.max_gaps}, min_severity={args.min_severity}")
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
        logger.info(f"Total traces: {len(all_traces)}")

        if not all_traces:
            logger.warning("No traces found. Exiting.")
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
            result = classifier.classify_gap(gap.failure_examples, max_samples=3)
            classifications[gap_key] = result
            logger.info(f"    {gap_key}: {result['category']} (confidence={result['confidence']})")

        # Step 3.6: Defer hard/ambiguous cases to the Hermes LLM judge (NEW)
        #
        # Only CODE_GAP_NEEDS_INVESTIGATION samples get a judge call — these
        # are cases where a rule genuinely can't diagnose the root cause
        # (entities matched but the answer is still IDK, e.g. the entities[0]
        # composition-bug pattern found earlier this session). Checks once
        # whether Hermes is even available before attempting any calls.
        hermes_available = is_hermes_available()
        logger.info(f"STEP 3.6: Hermes judge availability: {hermes_available}")
        judge_verdicts = {}

        if hermes_available:
            judge = HermesJudge(bridge=bridge)
            for gap_key, result in classifications.items():
                needs_judge = [
                    r for r in result["per_query_results"]
                    if r["category"] == CODE_GAP_NEEDS_INVESTIGATION
                ]
                if not needs_judge:
                    continue
                sample = needs_judge[0]
                gap = selected_gaps[int(gap_key.split("#")[1]) - 1]
                gap_summary = {
                    "module": gap.module,
                    "intent": gap.intent,
                    "failure_examples": [sample["query"]],
                    "entities_matched": sample["evidence"].get("entities", []),
                    "evidence_sources": sample["evidence"].get("evidence_sources", []),
                    "current_answer_preview": (sample["evidence"].get("answer") or "")[:300],
                    "deterministic_classification": sample["category"],
                }
                logger.info(f"  Judging {gap_key} ({gap.module}/{gap.intent})...")
                verdict = judge.judge_gap(gap_summary)
                judge_verdicts[gap_key] = verdict
                if verdict.get("degraded"):
                    logger.warning(f"    {gap_key}: judge degraded — {verdict['reasoning']}")
                else:
                    logger.info(f"    {gap_key}: {verdict['root_cause']} (confidence={verdict['confidence']})")
        else:
            logger.info("  Hermes not available — skipping judge calls for this run")

        # Step 3.7: Write actionable gaps to Hermes Kanban board
        logger.info("STEP 3.7: Writing actionable gaps to Kanban board")
        from .utils.kanban_writer import KanbanWriter
        kanban = KanbanWriter()
        archived = kanban.clear_board()
        logger.info(f"  Cleared {archived} stale task(s) from board")
        kanban_task_pairs = {}  # gap_key -> [(task_id, sub_category)]
        for i, gap in enumerate(selected_gaps, 1):
            gap_key = f"Gap #{i}"
            classification = classifications.get(gap_key, {})
            pairs = kanban.write_gap_tasks(i, gap, classification)
            if pairs:
                kanban_task_pairs[gap_key] = pairs
                task_ids = [p[0] for p in pairs]
                logger.info(f"  {gap_key}: created {len(pairs)} kanban task(s): {task_ids}")
            else:
                logger.info(f"  {gap_key}: no kanban task (category: {classification.get('category')})")

        # Step 3.8: Enrich kanban tasks with classification findings and judge verdicts
        logger.info("STEP 3.8: Enriching kanban tasks with findings")
        for gap_key, pairs in kanban_task_pairs.items():
            gap_idx = int(gap_key.split("#")[1]) - 1
            gap = selected_gaps[gap_idx]
            classification = classifications.get(gap_key, {})
            judge_verdict = judge_verdicts.get(gap_key)
            for task_id, sub_category in pairs:
                finding = kanban.build_finding(
                    sub_category=sub_category,
                    gap=gap,
                    classification=classification,
                    judge_verdict=judge_verdict,
                )
                if finding:
                    ok = kanban.post_hermes_finding(task_id, finding)
                    if ok:
                        logger.info(f"  Posted finding to {task_id} ({sub_category}, conf={finding.get('confidence')})")
                    else:
                        logger.warning(f"  Failed to post finding to {task_id}")

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
            judge_verdicts=judge_verdicts,
        )

        # Step 5: Write proposals document
        logger.info("STEP 5: Writing proposals document")
        proposals_writer = ProposalsWriter(
            output_dir=Path("local/supervisor/proposals")
        )
        tasks = proposals_writer.load_tasks()
        proposals_path = proposals_writer.write_document(tasks)
        logger.info(f"  Proposals written to: {proposals_path}")

        logger.info("=" * 80)
        logger.info("KB Supervisor Agent Completed Successfully")
        logger.info(f"Report: {report_path}")
        logger.info(f"Proposals: {proposals_path}")
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
        print(f"✓ Proposals: {proposals_path}  ← review & edit, then tell Claude 'apply proposals'")
        print(f"✓ Logs: {config.logs_dir / f'supervisor_{timestamp}.log'}")
        print("=" * 80 + "\n")

        return 0

    except Exception as e:
        logger.exception(f"Supervisor agent failed: {e}")
        print(f"\n✗ Supervisor agent failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
