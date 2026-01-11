"""Main evaluation orchestrator for running LLM evaluations."""

import logging
import time
from datetime import datetime
from typing import Dict, List, Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table

from ..models.config import ModelConfig
from ..models.ollama_client import OllamaClient
from ..prompts.strategies import get_strategy
from ..results.storage import EvaluationResult, ResultsStorage
from ..tasks.base import Task


logger = logging.getLogger(__name__)
console = Console()


class Evaluator:
    """Main orchestrator for running LLM evaluations.

    This class coordinates tasks, models, prompting strategies, and result storage
    to execute the complete evaluation pipeline.
    """

    def __init__(self, ollama_client: OllamaClient, storage: ResultsStorage):
        """Initialize the evaluator.

        Args:
            ollama_client: Ollama client for model interactions
            storage: Results storage manager
        """
        self.client = ollama_client
        self.storage = storage
        self.run_id = datetime.now().strftime("run_%Y-%m-%d_%H-%M-%S")

        logger.info(f"Evaluator initialized with run ID: {self.run_id}")

    def run_evaluation(
        self,
        tasks: List[Task],
        models: List[ModelConfig],
        skip_validation: bool = False
    ):
        """Run evaluations for all tasks and models.

        Args:
            tasks: List of Task objects to evaluate
            models: List of ModelConfig objects to use
            skip_validation: If True, skip Ollama connection check
        """
        # Validate Ollama connection
        if not skip_validation:
            console.print("\n[bold cyan]Checking Ollama connection...[/bold cyan]")
            if not self.client.test_connection():
                console.print(
                    "[bold red]Error:[/bold red] Could not connect to Ollama. "
                    "Make sure Ollama is running (try: ollama serve)"
                )
                return

        # Build evaluation matrix
        evaluations = self._build_evaluation_matrix(tasks, models)

        console.print(f"\n[bold green]Starting evaluation run: {self.run_id}[/bold green]")
        console.print(f"Total evaluations to run: [bold]{len(evaluations)}[/bold]\n")

        # Display evaluation plan
        self._display_evaluation_plan(evaluations)

        # Run evaluations with progress tracking
        self._run_evaluations_with_progress(evaluations)

        # Generate summary report
        console.print("\n[bold cyan]Generating summary report...[/bold cyan]")
        self.storage.save_summary_report(self.run_id)

        # Display summary
        self._display_summary()

        console.print(f"\n[bold green]Evaluation complete![/bold green]")
        console.print(f"Results saved in: {self.storage.raw_dir / self.run_id}\n")

    def _build_evaluation_matrix(
        self,
        tasks: List[Task],
        models: List[ModelConfig]
    ) -> List[Dict]:
        """Build the matrix of all evaluations to run.

        Args:
            tasks: List of tasks
            models: List of models

        Returns:
            List of evaluation configurations
        """
        evaluations = []
        skipped_tasks = []

        for task in tasks:
            # Skip incomplete tasks
            if not task.is_complete:
                skipped_tasks.append(task.id)
                logger.info(f"Skipping incomplete task: {task.id}")
                continue

            for model in models:
                # Get supported strategies for this model
                for strategy_name in model.supported_strategies:
                    evaluations.append({
                        "task": task,
                        "model": model,
                        "strategy": strategy_name
                    })

        # Log skipped tasks if any
        if skipped_tasks:
            console.print(
                f"[yellow]Note:[/yellow] Skipping {len(skipped_tasks)} incomplete task(s): "
                f"{', '.join(skipped_tasks)}\n"
            )

        return evaluations

    def _display_evaluation_plan(self, evaluations: List[Dict]):
        """Display a table showing the evaluation plan.

        Args:
            evaluations: List of evaluation configurations
        """
        table = Table(title="Evaluation Plan")
        table.add_column("Task", style="cyan")
        table.add_column("Model", style="magenta")
        table.add_column("Strategy", style="green")

        for eval_config in evaluations:
            table.add_row(
                eval_config["task"].name,
                eval_config["model"].display_name,
                eval_config["strategy"]
            )

        console.print(table)
        console.print()

    def _run_evaluations_with_progress(self, evaluations: List[Dict]):
        """Run all evaluations with progress tracking.

        Args:
            evaluations: List of evaluation configurations
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:

            task_progress = progress.add_task(
                "[cyan]Running evaluations...",
                total=len(evaluations)
            )

            for eval_config in evaluations:
                try:
                    result = self._run_single_evaluation(
                        eval_config["task"],
                        eval_config["model"],
                        eval_config["strategy"]
                    )
                    self.storage.save_result(result, run_id=self.run_id)

                except Exception as e:
                    logger.error(f"Evaluation failed: {e}")
                    console.print(
                        f"[bold red]Error:[/bold red] Failed to evaluate "
                        f"{eval_config['task'].id} with {eval_config['model'].name} "
                        f"using {eval_config['strategy']}: {e}"
                    )

                progress.update(task_progress, advance=1)

    def _run_single_evaluation(
        self,
        task: Task,
        model: ModelConfig,
        strategy_name: str
    ) -> EvaluationResult:
        """Run a single evaluation.

        Args:
            task: Task to evaluate
            model: Model to use
            strategy_name: Prompting strategy to apply

        Returns:
            EvaluationResult object
        """
        # Build prompt using strategy
        strategy = get_strategy(strategy_name)
        prompt = strategy.build_prompt(task)

        # Call Ollama to generate response
        start_time = time.time()
        try:
            response = self.client.generate(
                model=model.name,
                prompt=prompt,
                temperature=model.temperature,
                top_p=model.top_p,
                max_tokens=model.max_tokens
            )
            duration_ms = int((time.time() - start_time) * 1000)

            # Extract response text and metadata
            response_text = response.get("response", "")
            prompt_tokens = response.get("prompt_eval_count", 0)
            completion_tokens = response.get("eval_count", 0)

        except Exception as e:
            logger.error(f"Generation failed for {task.id}: {e}")
            # Create error result
            duration_ms = int((time.time() - start_time) * 1000)
            response_text = f"ERROR: {str(e)}"
            prompt_tokens = 0
            completion_tokens = 0

        # Create evaluation result
        result = EvaluationResult(
            task_id=task.id,
            model_name=model.name,
            strategy=strategy_name,
            prompt=prompt,
            response=response_text,
            timestamp=datetime.now().isoformat(),
            model_config=model.to_dict(),
            generation_time_ms=duration_ms,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens
        )

        logger.info(
            f"Completed: {task.id} | {model.name} | {strategy_name} "
            f"({duration_ms}ms, {completion_tokens} tokens)"
        )

        return result

    def _display_summary(self):
        """Display a summary of the evaluation run."""
        summary = self.storage.generate_summary_report(run_id=self.run_id)

        table = Table(title=f"Evaluation Summary - {self.run_id}")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Total Evaluations", str(summary.get("total_evaluations", 0)))
        table.add_row("Tasks", str(len(summary.get("tasks", []))))
        table.add_row("Models", str(len(summary.get("models", []))))
        table.add_row("Strategies", str(len(summary.get("strategies", []))))
        table.add_row(
            "Total Generation Time",
            f"{summary.get('total_generation_time_sec', 0):.2f}s"
        )
        table.add_row(
            "Average Generation Time",
            f"{summary.get('average_generation_time_sec', 0):.2f}s"
        )
        table.add_row("Total Tokens Generated", str(summary.get("total_tokens_generated", 0)))

        console.print("\n", table, "\n")

    def run_single_task(
        self,
        task: Task,
        model: ModelConfig,
        strategy_name: str
    ) -> EvaluationResult:
        """Run a single evaluation and return the result without saving.

        Useful for testing or interactive evaluation.

        Args:
            task: Task to evaluate
            model: Model to use
            strategy_name: Prompting strategy

        Returns:
            EvaluationResult object
        """
        return self._run_single_evaluation(task, model, strategy_name)
