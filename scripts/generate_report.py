#!/usr/bin/env python3
"""Generate CSV report from evaluation run results.

This script should be run AFTER you've manually filled in the scores
in the JSON files. It will:
1. Calculate total_score for each result by summing the scores dict
2. Update the JSON files with calculated total_score
3. Generate a CSV file with all results for analysis

Usage:
    python scripts/generate_report.py <run_id>
    python scripts/generate_report.py run_2026-01-11_15-30-45

    Or use --latest to process the most recent run:
    python scripts/generate_report.py --latest
"""

import argparse
import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

from llm_eval.results.storage import ResultsStorage


console = Console()


def setup_logging(verbose: bool = False):
    """Setup logging configuration.

    Args:
        verbose: If True, set log level to DEBUG
    """
    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True, console=console)]
    )


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate CSV report from evaluation run after manual scoring"
    )

    parser.add_argument(
        "run_id",
        nargs="?",
        type=str,
        help="Run ID to generate report for (e.g., run_2026-01-11_15-30-45)"
    )

    parser.add_argument(
        "--latest",
        action="store_true",
        help="Use the most recent run"
    )

    parser.add_argument(
        "--results-dir",
        type=Path,
        default=Path("data/results"),
        help="Directory where results are stored (default: data/results)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    return parser.parse_args()


def display_run_summary(storage: ResultsStorage, run_id: str):
    """Display summary of the run before processing.

    Args:
        storage: ResultsStorage instance
        run_id: Run identifier
    """
    results = storage.load_results(run_id=run_id)

    if not results:
        console.print(f"[bold red]Error:[/bold red] No results found for run: {run_id}")
        return False

    scored_count = sum(1 for r in results if r.scores is not None)
    unscored_count = sum(1 for r in results if r.scores is None)

    table = Table(title=f"Run Summary: {run_id}")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Total Results", str(len(results)))
    table.add_row("Scored Results", str(scored_count))
    table.add_row("Unscored Results", str(unscored_count))

    console.print("\n", table, "\n")

    if unscored_count > 0:
        console.print(
            f"[bold yellow]Warning:[/bold yellow] {unscored_count} result(s) "
            "do not have scores filled in yet.\n"
            "The CSV will include these, but they will have empty score columns.\n"
        )

    return True


def main():
    """Main entry point."""
    args = parse_args()

    # Setup logging
    setup_logging(args.verbose)

    # Initialize storage
    storage = ResultsStorage(base_path=args.results_dir)

    # Determine run_id
    if args.latest:
        run_id = storage.get_latest_run_id()
        if run_id is None:
            console.print("[bold red]Error:[/bold red] No runs found")
            return 1
        console.print(f"[cyan]Using latest run:[/cyan] {run_id}\n")
    elif args.run_id:
        run_id = args.run_id
    else:
        console.print("[bold red]Error:[/bold red] Please provide run_id or use --latest")
        return 1

    # Display summary
    if not display_run_summary(storage, run_id):
        return 1

    # Step 1: Calculate and update total_scores
    console.print("[bold cyan]Step 1:[/bold cyan] Calculating total_score for all results...\n")
    updated_count = storage.calculate_and_update_total_scores(run_id)

    if updated_count > 0:
        console.print(f"[green]Updated total_score in {updated_count} JSON file(s)[/green]\n")
    else:
        console.print("[yellow]No results with scores found to calculate totals[/yellow]\n")

    # Step 2: Generate CSV
    console.print("[bold cyan]Step 2:[/bold cyan] Generating CSV report...\n")
    csv_path = storage.reports_dir / f"{run_id}_results.csv"
    storage.export_to_csv(csv_path, run_id=run_id)

    console.print(f"[bold green]Report generated successfully![/bold green]")
    console.print(f"CSV saved to: {csv_path}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
