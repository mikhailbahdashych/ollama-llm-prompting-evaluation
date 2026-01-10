"""Reading Comprehension task definition."""

from ..base import Task, TaskExample


def create_reading_comprehension_task() -> Task:
    """Create the Reading Comprehension evaluation task.

    This task evaluates the model's ability to understand and extract
    information from a given text passage.
    """
    return Task(
        id="reading_comprehension",
        name="Reading Comprehension",
        category="Understanding",
        description="[TODO: Add description of reading comprehension requirements]",
        evaluation_input="[TODO: Add passage and comprehension question]",
        expected_output_characteristics="[TODO: Describe what demonstrates good comprehension]",
        development_examples=[
            TaskExample(
                input="[TODO: Example passage and question 1]",
                output="[TODO: Example answer showing comprehension 1]",
                explanation="[TODO: Why this answer demonstrates understanding]"
            ),
            TaskExample(
                input="[TODO: Example passage and question 2]",
                output="[TODO: Example answer showing comprehension 2]"
            )
        ],
        evaluation_criteria={
            "accuracy": "Answer correctly reflects passage content",
            "completeness": "Answer addresses the full question",
            "evidence_based": "Answer is grounded in the text",
            "clarity": "Answer is clearly expressed"
        },
        scoring_rubric={
            "accuracy": 10,
            "completeness": 5,
            "evidence_based": 3,
            "clarity": 2
        }
    )
