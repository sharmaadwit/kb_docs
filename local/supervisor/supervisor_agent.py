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

        # Step 4: Generate report
        logger.info("STEP 4: Generating report with Qwen analysis")
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
        report_text = generator.generate_report(selected_gaps, all_traces, report_path)

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
