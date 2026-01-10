"""Logical Reasoning task definition."""

from ..base import Task, TaskExample


def create_logical_reasoning_task() -> Task:
    """Create the Logical Reasoning evaluation task.

    This task evaluates the model's ability to apply logical rules
    and derive valid conclusions.
    """
    return Task(
        id="logical_reasoning",
        name="Logical Reasoning",
        category="Reasoning",
        description="[TODO: Add description of what this task tests - logical deduction and inference]",
        evaluation_input="[TODO: Add actual logical reasoning problem]",
        expected_output_characteristics="[TODO: Describe what logical reasoning should demonstrate]",
        development_examples=[
            TaskExample(
                input="[TODO: Example logical reasoning input 1]",
                output="[TODO: Example output with valid logical reasoning 1]",
                explanation="[TODO: Why this reasoning is logically valid]"
            ),
            TaskExample(
                input="[TODO: Example logical reasoning input 2]",
                output="[TODO: Example output with valid logical reasoning 2]"
            )
        ],
        evaluation_criteria={
            "logical_validity": "Reasoning follows logical rules and principles",
            "completeness": "Addresses all aspects of the problem",
            "clarity": "Explanation is clear and well-structured"
        },
        scoring_rubric={
            "logical_validity": 10,
            "completeness": 5,
            "clarity": 5
        },
        difficulty="medium",
        notes="TODO: Fill in actual content later. Include syllogisms or logical puzzles."
    )
