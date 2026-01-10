"""Code Generation task definition."""

from ..base import Task, TaskExample


def create_code_generation_task() -> Task:
    """Create the Code Generation evaluation task.

    This task evaluates the model's ability to write correct,
    efficient, and well-structured code.
    """
    return Task(
        id="code_generation",
        name="Code Generation",
        category="Programming",
        description="[TODO: Add description of code generation requirements]",
        evaluation_input="[TODO: Add actual coding problem]",
        expected_output_characteristics="[TODO: Describe what makes good code solution]",
        development_examples=[
            TaskExample(
                input="[TODO: Example coding problem 1]",
                output="[TODO: Example code solution 1]",
                explanation="[TODO: Why this is a good solution]"
            ),
            TaskExample(
                input="[TODO: Example coding problem 2]",
                output="[TODO: Example code solution 2]"
            )
        ],
        evaluation_criteria={
            "correctness": "Code solves the problem correctly",
            "code_quality": "Code is clean, readable, and well-structured",
            "efficiency": "Solution is reasonably efficient",
            "documentation": "Code includes appropriate comments/docstrings"
        },
        scoring_rubric={
            "correctness": 10,
            "code_quality": 5,
            "efficiency": 3,
            "documentation": 2
        }
    )
