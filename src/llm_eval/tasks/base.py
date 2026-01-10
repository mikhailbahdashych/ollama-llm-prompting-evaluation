"""Base classes for task definitions."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class TaskExample:
    """Represents a single example for few-shot learning.

    Attributes:
        input: The input text/problem for the example
        output: The expected output/solution for the example
        explanation: Optional explanation of why this is the correct output
    """
    input: str
    output: str
    explanation: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "input": self.input,
            "output": self.output,
            "explanation": self.explanation
        }


@dataclass
class Task:
    """Base task definition.

    This class defines the structure for evaluation tasks. Tasks with [TODO: ...]
    markers should be filled in later with actual task content.

    Attributes:
        id: Unique identifier for the task (e.g., "logical_reasoning")
        name: Human-readable name (e.g., "Logical Reasoning")
        category: Task category/type
        description: Description of what the task tests
        evaluation_input: The actual problem/task to solve
        expected_output_characteristics: Description of what good output looks like
        development_examples: List of examples for few-shot prompting (2-3 recommended)
        evaluation_criteria: Dict of criterion_name -> description
        scoring_rubric: Dict of aspect -> maximum_points
        difficulty: Task difficulty level (easy, medium, hard)
        notes: Additional notes or TODOs for the task
    """
    id: str
    name: str
    category: str
    description: str
    evaluation_input: str
    expected_output_characteristics: str
    development_examples: List[TaskExample] = field(default_factory=list)
    evaluation_criteria: Dict[str, str] = field(default_factory=dict)
    scoring_rubric: Dict[str, int] = field(default_factory=dict)
    difficulty: str = "medium"
    notes: str = ""

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "evaluation_input": self.evaluation_input,
            "expected_output_characteristics": self.expected_output_characteristics,
            "development_examples": [ex.to_dict() for ex in self.development_examples],
            "evaluation_criteria": self.evaluation_criteria,
            "scoring_rubric": self.scoring_rubric,
            "difficulty": self.difficulty,
            "notes": self.notes
        }

    def get_max_score(self) -> int:
        """Calculate the maximum possible score for this task."""
        return sum(self.scoring_rubric.values())

    def is_complete(self) -> bool:
        """Check if task definition is complete (no TODO markers)."""
        fields_to_check = [
            self.description,
            self.evaluation_input,
            self.expected_output_characteristics,
            self.notes
        ]
        return not any("[TODO" in str(field) for field in fields_to_check)

    def get_incomplete_fields(self) -> List[str]:
        """Return list of field names that still have TODO markers."""
        incomplete = []
        if "[TODO" in self.description:
            incomplete.append("description")
        if "[TODO" in self.evaluation_input:
            incomplete.append("evaluation_input")
        if "[TODO" in self.expected_output_characteristics:
            incomplete.append("expected_output_characteristics")
        if any("[TODO" in ex.input or "[TODO" in ex.output for ex in self.development_examples):
            incomplete.append("development_examples")
        return incomplete
