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
        description="This task evaluates the model's ability to carefully follow multiple specific instructions and constraints while completing a task. It tests attention to detail and instruction adherence.",
        evaluation_input="""Write a brief description of a smartphone for a product catalog. Your description must follow ALL of these constraints:

1. The description must be EXACTLY 4 sentences long (no more, no less)
2. The first sentence must start with the word "Introducing"
3. You must mention exactly THREE features (battery, camera, display)
4. Do NOT use the words "amazing", "incredible", or "revolutionary"
5. End the description with a question
6. Use at least one comparison (e.g., "faster than", "brighter than")

Write the product description now.""",
        expected_output_characteristics="A product description that follows all six constraints precisely: exactly 4 sentences, starts with 'Introducing', mentions battery/camera/display, avoids forbidden words, ends with a question, and includes at least one comparison. The text should be coherent and readable while satisfying all constraints.",
        development_examples=[
            TaskExample(
                input="""Write a short poem about winter. Follow these rules:
1. The poem must be exactly 3 lines long
2. Each line must have exactly 5 words
3. The last word must rhyme with "snow"
4. Do not use the word "cold"

Write the poem now.""",
                output="""Winter brings the soft white snow
Children play and watch it glow
Nature puts on quite a show""",
                explanation="This output correctly follows all four constraints: 3 lines, 5 words per line, ends with 'snow' (rhyming with itself), and doesn't use 'cold'. The poem is coherent while meeting all requirements."
            ),
            TaskExample(
                input="""Describe a coffee shop in 2 sentences. Requirements:
1. First sentence must mention the word "aroma"
2. Second sentence must be a question
3. Use exactly one adjective in each sentence
4. Do not use the word "delicious"

Write the description.""",
                output="""The rich aroma fills the cozy space as customers arrive. Would you like to experience this welcoming atmosphere?""",
                explanation="Follows all constraints: mentions 'aroma' in first sentence, second sentence is a question, one adjective per sentence (rich, welcoming), and avoids 'delicious'."
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
        },
        is_complete=True
    )
