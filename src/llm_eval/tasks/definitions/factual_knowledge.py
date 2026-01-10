"""Factual Knowledge & Retrieval task definition."""

from ..base import Task, TaskExample


def create_factual_knowledge_task() -> Task:
    """Create the Factual Knowledge & Retrieval evaluation task.

    This task evaluates the model's ability to recall and apply
    factual information accurately.
    """
    return Task(
        id="factual_knowledge",
        name="Factual Knowledge & Retrieval",
        category="Knowledge",
        description="[TODO: Add description of factual knowledge requirements]",
        evaluation_input="[TODO: Add actual factual knowledge question]",
        expected_output_characteristics="[TODO: Describe what constitutes accurate factual response]",
        development_examples=[
            TaskExample(
                input="[TODO: Example factual question 1]",
                output="[TODO: Example accurate factual answer 1]",
                explanation="[TODO: Why this answer is factually correct]"
            ),
            TaskExample(
                input="[TODO: Example factual question 2]",
                output="[TODO: Example accurate factual answer 2]"
            )
        ],
        evaluation_criteria={
            "accuracy": "Information is factually correct",
            "completeness": "Answer includes relevant details",
            "specificity": "Provides specific, not vague information",
            "source_reliability": "Information comes from reliable knowledge"
        },
        scoring_rubric={
            "accuracy": 10,
            "completeness": 5,
            "specificity": 3,
            "source_reliability": 2
        }
    )
