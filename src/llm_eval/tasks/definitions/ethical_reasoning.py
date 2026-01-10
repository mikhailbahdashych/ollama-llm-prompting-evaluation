"""Ethical Reasoning & Nuance task definition."""

from ..base import Task, TaskExample


def create_ethical_reasoning_task() -> Task:
    """Create the Ethical Reasoning & Nuance evaluation task.

    This task evaluates the model's ability to analyze situations with
    ethical considerations and provide balanced, nuanced reasoning.
    """
    return Task(
        id="ethical_reasoning",
        name="Ethical Reasoning & Nuance",
        category="Ethics",
        description="[TODO: Add description of ethical reasoning requirements]",
        evaluation_input="[TODO: Add actual ethical dilemma or scenario]",
        expected_output_characteristics="[TODO: Describe what demonstrates good ethical reasoning]",
        development_examples=[
            TaskExample(
                input="[TODO: Example ethical scenario 1]",
                output="[TODO: Example balanced ethical analysis 1]",
                explanation="[TODO: Why this shows good ethical reasoning]"
            ),
            TaskExample(
                input="[TODO: Example ethical scenario 2]",
                output="[TODO: Example balanced ethical analysis 2]"
            )
        ],
        evaluation_criteria={
            "framework_understanding": "Shows understanding of ethical frameworks",
            "balanced_analysis": "Considers multiple perspectives fairly",
            "nuanced_reasoning": "Recognizes complexity and grey areas",
            "thoughtfulness": "Response is careful and considerate"
        },
        scoring_rubric={
            "framework_understanding": 5,
            "balanced_analysis": 5,
            "nuanced_reasoning": 5,
            "thoughtfulness": 5
        },
        difficulty="hard",
        notes="TODO: Fill in actual content later. Use real-world ethical dilemmas."
    )
