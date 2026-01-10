"""Mathematical Problem Solving task definition."""

from ..base import Task, TaskExample


def create_math_solving_task() -> Task:
    """Create the Mathematical Problem Solving evaluation task.

    This task evaluates the model's ability to solve mathematical
    problems with correct procedures and accurate results.
    """
    return Task(
        id="math_solving",
        name="Mathematical Problem Solving",
        category="Mathematics",
        description="[TODO: Add description of mathematical problem-solving requirements]",
        evaluation_input="[TODO: Add actual math problem]",
        expected_output_characteristics="[TODO: Describe what makes a good math solution]",
        development_examples=[
            TaskExample(
                input="[TODO: Example math problem 1]",
                output="[TODO: Example solution with steps 1]",
                explanation="[TODO: Why this solution is correct]"
            ),
            TaskExample(
                input="[TODO: Example math problem 2]",
                output="[TODO: Example solution with steps 2]"
            )
        ],
        evaluation_criteria={
            "correctness": "Final answer is mathematically correct",
            "methodology": "Uses appropriate mathematical methods",
            "step_clarity": "Steps are clearly shown and logical",
            "explanation": "Solution is well-explained"
        },
        scoring_rubric={
            "correctness": 10,
            "methodology": 5,
            "step_clarity": 3,
            "explanation": 2
        },
        difficulty="medium",
        notes="TODO: Fill in actual content later. Include algebra, geometry, or word problems."
    )
