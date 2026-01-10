"""Creative Writing task definition."""

from ..base import Task, TaskExample


def create_creative_writing_task() -> Task:
    """Create the Creative Writing evaluation task.

    This task evaluates the model's ability to generate creative,
    engaging, and well-structured narrative content.
    """
    return Task(
        id="creative_writing",
        name="Creative Writing",
        category="Generation",
        description="[TODO: Add description of creative writing requirements]",
        evaluation_input="[TODO: Add actual creative writing prompt]",
        expected_output_characteristics="[TODO: Describe what makes good creative writing]",
        development_examples=[
            TaskExample(
                input="[TODO: Example creative writing prompt 1]",
                output="[TODO: Example creative output 1]",
                explanation="[TODO: Why this demonstrates good creative writing]"
            ),
            TaskExample(
                input="[TODO: Example creative writing prompt 2]",
                output="[TODO: Example creative output 2]"
            )
        ],
        evaluation_criteria={
            "creativity": "Original and imaginative content",
            "coherence": "Story flows logically and maintains consistency",
            "engagement": "Writing is compelling and well-paced",
            "language_quality": "Good use of language and style"
        },
        scoring_rubric={
            "creativity": 5,
            "coherence": 5,
            "engagement": 5,
            "language_quality": 5
        },
        difficulty="medium",
        notes="TODO: Fill in actual content later. Could be story, poem, or descriptive passage."
    )
