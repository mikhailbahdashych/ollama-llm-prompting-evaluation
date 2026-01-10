"""Common Sense Reasoning task definition."""

from ..base import Task, TaskExample


def create_common_sense_task() -> Task:
    """Create the Common Sense Reasoning evaluation task.

    This task evaluates the model's ability to apply everyday knowledge
    and common sense to practical situations.
    """
    return Task(
        id="common_sense",
        name="Common Sense Reasoning",
        category="Reasoning",
        description="[TODO: Add description of common sense reasoning requirements]",
        evaluation_input="[TODO: Add actual common sense reasoning problem]",
        expected_output_characteristics="[TODO: Describe what demonstrates good common sense]",
        development_examples=[
            TaskExample(
                input="[TODO: Example common sense question 1]",
                output="[TODO: Example answer with common sense reasoning 1]",
                explanation="[TODO: Why this demonstrates common sense]"
            ),
            TaskExample(
                input="[TODO: Example common sense question 2]",
                output="[TODO: Example answer with common sense reasoning 2]"
            )
        ],
        evaluation_criteria={
            "practical_reasoning": "Applies real-world knowledge appropriately",
            "plausibility": "Answer is realistic and makes sense",
            "explanation_quality": "Reasoning is well-explained"
        },
        scoring_rubric={
            "practical_reasoning": 10,
            "plausibility": 5,
            "explanation_quality": 5
        }
    )
