"""Results storage and persistence for evaluation outputs."""

import json
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd


logger = logging.getLogger(__name__)


@dataclass
class EvaluationResult:
    """Single evaluation result.

    This class stores all information about a single evaluation run,
    including the prompt, response, metadata, and scores (filled in later).
    """
    # Identifiers
    task_id: str
    model_name: str
    strategy: str

    # Input/Output
    prompt: str
    response: str

    # Metadata
    timestamp: str
    model_config: Dict[str, Any] = field(default_factory=dict)

    # Performance metrics
    generation_time_ms: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0

    # Evaluation (filled in manually later)
    scores: Optional[Dict[str, int]] = None
    total_score: Optional[int] = None
    evaluator_notes: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: Dict) -> "EvaluationResult":
        """Create from dictionary."""
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> "EvaluationResult":
        """Create from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)


class ResultsStorage:
    """Manager for storing and retrieving evaluation results.

    Results are stored as JSON files in a hierarchical directory structure.
    """

    def __init__(self, base_path: Path):
        """Initialize results storage.

        Args:
            base_path: Base directory for storing results (e.g., data/results)
        """
        self.base_path = Path(base_path)
        self.raw_dir = self.base_path / "raw"
        self.scored_dir = self.base_path / "scored"
        self.reports_dir = self.base_path / "reports"

        # Create directories if they don't exist
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.scored_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Results storage initialized at: {self.base_path}")

    def save_result(self, result: EvaluationResult, run_id: Optional[str] = None) -> Path:
        """Save a single evaluation result as JSON.

        Args:
            result: The EvaluationResult to save
            run_id: Optional run identifier for organizing results

        Returns:
            Path to the saved file
        """
        # Generate run ID if not provided
        if run_id is None:
            run_id = datetime.now().strftime("run_%Y-%m-%d_%H-%M-%S")

        # Create run-specific directory
        run_dir = self.raw_dir / run_id
        run_dir.mkdir(exist_ok=True)

        # Generate filename: {task_id}_{model}_{strategy}.json
        model_short = result.model_name.replace(":", "_").replace("/", "_")
        filename = f"{result.task_id}_{model_short}_{result.strategy}.json"
        filepath = run_dir / filename

        # Save to file
        with open(filepath, 'w') as f:
            f.write(result.to_json())

        logger.debug(f"Saved result to: {filepath}")
        return filepath

    def load_result(self, filepath: Path) -> Optional[EvaluationResult]:
        """Load a single result from JSON file.

        Args:
            filepath: Path to the JSON file

        Returns:
            EvaluationResult if successful, None otherwise
        """
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return EvaluationResult.from_dict(data)
        except Exception as e:
            logger.error(f"Failed to load result from {filepath}: {e}")
            return None

    def load_results(
        self,
        run_id: Optional[str] = None,
        task_id: Optional[str] = None,
        model_name: Optional[str] = None,
        strategy: Optional[str] = None
    ) -> List[EvaluationResult]:
        """Load results with optional filtering.

        Args:
            run_id: Filter by specific run ID
            task_id: Filter by task ID
            model_name: Filter by model name
            strategy: Filter by strategy name

        Returns:
            List of matching EvaluationResult objects
        """
        results = []

        # Determine which directories to search
        if run_id:
            search_dirs = [self.raw_dir / run_id]
        else:
            search_dirs = [d for d in self.raw_dir.iterdir() if d.is_dir()]

        # Load all JSON files from search directories
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue

            for filepath in search_dir.glob("*.json"):
                result = self.load_result(filepath)
                if result is None:
                    continue

                # Apply filters
                if task_id and result.task_id != task_id:
                    continue
                if model_name and result.model_name != model_name:
                    continue
                if strategy and result.strategy != strategy:
                    continue

                results.append(result)

        logger.info(f"Loaded {len(results)} results")
        return results

    def export_to_csv(self, output_path: Path, run_id: Optional[str] = None):
        """Export results to CSV for analysis.

        Args:
            output_path: Path for the CSV file
            run_id: Optional run ID to export (if None, exports all)
        """
        results = self.load_results(run_id=run_id)

        if not results:
            logger.warning("No results to export")
            return

        # Convert to list of dicts
        data = [result.to_dict() for result in results]

        # Create DataFrame
        df = pd.DataFrame(data)

        # Save to CSV
        df.to_csv(output_path, index=False)
        logger.info(f"Exported {len(results)} results to: {output_path}")

    def generate_summary_report(self, run_id: Optional[str] = None) -> Dict:
        """Generate summary statistics for results.

        Args:
            run_id: Optional run ID to summarize

        Returns:
            Dictionary with summary statistics
        """
        results = self.load_results(run_id=run_id)

        if not results:
            return {"error": "No results found"}

        summary = {
            "total_evaluations": len(results),
            "tasks": list(set(r.task_id for r in results)),
            "models": list(set(r.model_name for r in results)),
            "strategies": list(set(r.strategy for r in results)),
            "total_generation_time_sec": sum(r.generation_time_ms for r in results) / 1000,
            "average_generation_time_sec": sum(r.generation_time_ms for r in results) / len(results) / 1000,
            "total_tokens_generated": sum(r.completion_tokens for r in results),
            "evaluated_results": sum(1 for r in results if r.scores is not None),
            "pending_evaluation": sum(1 for r in results if r.scores is None)
        }

        return summary

    def save_summary_report(self, run_id: str):
        """Generate and save a summary report.

        Args:
            run_id: Run identifier
        """
        summary = self.generate_summary_report(run_id)

        # Save as JSON
        report_path = self.reports_dir / f"{run_id}_summary.json"
        with open(report_path, 'w') as f:
            json.dump(summary, f, indent=2)

        logger.info(f"Summary report saved to: {report_path}")

        # Also export to CSV
        csv_path = self.reports_dir / f"{run_id}_results.csv"
        self.export_to_csv(csv_path, run_id=run_id)

    def get_latest_run_id(self) -> Optional[str]:
        """Get the most recent run ID.

        Returns:
            Run ID string or None if no runs exist
        """
        run_dirs = [d for d in self.raw_dir.iterdir() if d.is_dir()]
        if not run_dirs:
            return None

        latest = max(run_dirs, key=lambda d: d.stat().st_mtime)
        return latest.name
