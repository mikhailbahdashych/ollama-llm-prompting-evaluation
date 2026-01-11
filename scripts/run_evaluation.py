#!/usr/bin/env python3
"""Main script to run LLM evaluations.

This script orchestrates the complete evaluation pipeline:
1. Loads all task definitions
2. Loads model configurations
3. Runs evaluations for all task-model-strategy combinations
4. Saves results and generates reports
"""

import argparse
import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console
from rich.logging import RichHandler

from llm_eval.evaluation.evaluator import Evaluator
from llm_eval.models.config import MODELS, get_all_models
from llm_eval.models.ollama_client import OllamaClient
from llm_eval.results.storage import ResultsStorage
from llm_eval.tasks.registry import TaskRegistry


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
        description="Run LLM evaluation across tasks, models, and prompting strategies"
    )

    parser.add_argument(
        "--tasks",
        type=str,
        help="Comma-separated list of task IDs to run (default: all)",
        default=None
    )

    parser.add_argument(
        "--models",
        type=str,
        help="Comma-separated list of model keys to run (default: all)",
        default=None
    )

    parser.add_argument(
        "--ollama-url",
        type=str,
        default="http://localhost:11434",
        help="Ollama API base URL (default: http://localhost:11434)"
    )

    parser.add_argument(
        "--results-dir",
        type=Path,
        default=Path("data/results"),
        help="Directory to store results (default: data/results)"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip Ollama connection validation"
    )

    parser.add_argument(
        "--list-tasks",
        action="store_true",
        help="List all available tasks and exit"
    )

    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List all configured models and exit"
    )

    parser.add_argument(
        "--validate-tasks",
        action="store_true",
        help="Validate task definitions and show completion status"
    )

    return parser.parse_args()


def list_tasks(registry: TaskRegistry):
    """Display all available tasks."""
    from rich.table import Table

    table = Table(title="Available Tasks")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Category", style="magenta")
    table.add_column("Complete", style="bold")

    for task in registry.get_all_tasks():
        complete = "Yes" if task.is_complete else "No"
        complete_style = "green" if task.is_complete else "red"
        table.add_row(
            task.id,
            task.name,
            task.category,
            f"[{complete_style}]{complete}[/{complete_style}]"
        )

    console.print(table)
    console.print(f"\nTotal tasks: {len(registry.get_all_tasks())}")
    console.print(f"Complete: {registry.count_complete_tasks()}")
    console.print(f"Incomplete: {registry.count_incomplete_tasks()}\n")


def list_models():
    """Display all configured models."""
    from rich.table import Table

    table = Table(title="Configured Models")
    table.add_column("Key", style="cyan")
    table.add_column("Model", style="green")
    table.add_column("Display Name", style="magenta")
    table.add_column("Size", style="yellow")
    table.add_column("Reasoning", style="blue")
    table.add_column("Strategies", style="white")

    for key, model in MODELS.items():
        reasoning = "Yes" if model.is_reasoning_model else "No"
        strategies = ", ".join(model.supported_strategies)
        table.add_row(
            key,
            model.name,
            model.display_name,
            model.parameters,
            reasoning,
            strategies
        )

    console.print(table)
    console.print(f"\nTotal models: {len(MODELS)}\n")


def validate_tasks(registry: TaskRegistry):
    """Validate all task definitions and show completion status."""
    from rich.table import Table

    all_tasks = registry.get_all_tasks()
    completion_status = registry.get_completion_status()

    table = Table(title="Task Completion Status")
    table.add_column("Task ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Status", style="bold")

    for task in all_tasks:
        status = "Complete" if task.is_complete else "Incomplete"
        status_style = "green" if task.is_complete else "red"
        table.add_row(
            task.id,
            task.name,
            f"[{status_style}]{status}[/{status_style}]"
        )

    console.print(table)
    console.print(f"\nTotal tasks: {len(all_tasks)}")
    console.print(f"Complete: {registry.count_complete_tasks()}")
    console.print(f"Incomplete: {registry.count_incomplete_tasks()}")

    if registry.count_incomplete_tasks() == 0:
        console.print("\n[bold green]All tasks are complete![/bold green]\n")
    else:
        console.print(
            f"\n[bold yellow]Note:[/bold yellow] Incomplete tasks will be skipped "
            "during evaluation runs.\n"
        )


def main():
    """Main entry point."""
    args = parse_args()

    # Setup logging
    setup_logging(args.verbose)

    # Initialize task registry
    console.print("[bold cyan]Loading tasks...[/bold cyan]")
    registry = TaskRegistry()

    # Handle list/validation commands
    if args.list_tasks:
        list_tasks(registry)
        return

    if args.list_models:
        list_models()
        return

    if args.validate_tasks:
        validate_tasks(registry)
        return

    # Filter tasks if specified
    if args.tasks:
        task_ids = [t.strip() for t in args.tasks.split(",")]
        tasks = [registry.get_task(tid) for tid in task_ids]
        tasks = [t for t in tasks if t is not None]  # Remove None values

        if not tasks:
            console.print(f"[bold red]Error:[/bold red] No valid tasks found in: {args.tasks}")
            return
    else:
        tasks = registry.get_all_tasks()

    # Filter models if specified
    if args.models:
        model_keys = [m.strip() for m in args.models.split(",")]
        models = []
        for key in model_keys:
            if key in MODELS:
                models.append(MODELS[key])
            else:
                console.print(f"[bold yellow]Warning:[/bold yellow] Unknown model key: {key}")

        if not models:
            console.print(f"[bold red]Error:[/bold red] No valid models found in: {args.models}")
            return
    else:
        models = get_all_models()

    # Initialize components
    console.print("[bold cyan]Initializing evaluation system...[/bold cyan]")
    client = OllamaClient(base_url=args.ollama_url)
    storage = ResultsStorage(base_path=args.results_dir)
    evaluator = Evaluator(client, storage)

    # Run evaluations
    evaluator.run_evaluation(
        tasks=tasks,
        models=models,
        skip_validation=args.skip_validation
    )


if __name__ == "__main__":
    main()
