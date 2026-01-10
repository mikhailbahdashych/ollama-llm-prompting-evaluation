"""Language Understanding & Ambiguity task definition."""

from ..base import Task, TaskExample


def create_language_understanding_task() -> Task:
    """Create the Language Understanding & Ambiguity evaluation task.

    This task evaluates the model's ability to handle ambiguous language,
    understand nuances, and resolve linguistic ambiguity.
    """
    return Task(
        id="language_understanding",
        name="Language Understanding & Ambiguity",
        category="Understanding",
        description="[TODO: Add description of language understanding requirements]",
        evaluation_input="[TODO: Add actual ambiguous language problem]",
        expected_output_characteristics="[TODO: Describe what shows good language understanding]",
        development_examples=[
            TaskExample(
                input="[TODO: Example ambiguous statement 1]",
                output="[TODO: Example interpretation showing understanding 1]",
                explanation="[TODO: Why this interpretation is correct]"
            ),
            TaskExample(
                input="[TODO: Example ambiguous statement 2]",
                output="[TODO: Example interpretation showing understanding 2]"
            )
        ],
        evaluation_criteria={
            "disambiguation": "Correctly identifies and resolves ambiguity",
            "nuance_recognition": "Recognizes subtle meanings and implications",
            "explanation_clarity": "Clearly explains the interpretation"
        },
        scoring_rubric={
            "disambiguation": 10,
            "nuance_recognition": 5,
            "explanation_clarity": 5
        },
        difficulty="medium",
        notes="TODO: Fill in actual content later. Include ambiguous sentences or idioms."
    )
