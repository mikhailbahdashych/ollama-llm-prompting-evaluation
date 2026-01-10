"""Instruction Following task definition."""

from ..base import Task, TaskExample


def create_instruction_following_task() -> Task:
    """Create the Instruction Following evaluation task.

    This task evaluates the model's ability to follow specific instructions
    and constraints in its response.
    """
    return Task(
        id="instruction_following",
        name="Instruction Following",
        category="IFEval-style",
        description="[TODO: Add description of what this task tests - ability to follow complex instructions]",
        evaluation_input="[TODO: Add actual instruction-following problem with specific constraints]",
        expected_output_characteristics="[TODO: Describe what a good response should include]",
        development_examples=[
            TaskExample(
                input="[TODO: Example instruction-following input 1]",
                output="[TODO: Example output that correctly follows instructions 1]",
                explanation="[TODO: Why this output correctly follows all instructions]"
            ),
            TaskExample(
                input="[TODO: Example instruction-following input 2]",
                output="[TODO: Example output that correctly follows instructions 2]"
            )
        ],
        evaluation_criteria={
            "instruction_adherence": "Follows all given instructions and constraints",
            "completeness": "Addresses all parts of the instructions",
            "format_compliance": "Response matches required format"
        },
        scoring_rubric={
            "instruction_adherence": 10,
            "completeness": 5,
            "format_compliance": 5
        }
    )
