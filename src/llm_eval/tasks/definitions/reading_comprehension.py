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
        description="This task evaluates the model's ability to carefully read and understand a text passage, extract relevant information, make inferences based on the text, and provide accurate, evidence-based answers to questions.",
        evaluation_input="""Read the following passage carefully:

The concept of neuroplasticity has revolutionized our understanding of the human brain. For decades, scientists believed that the brain's structure was fixed after childhood, with neural pathways set in stone by early adulthood. However, research over the past thirty years has revealed that the brain remains remarkably adaptable throughout life. When we learn new skills, form memories, or recover from injury, our brains physically change by forming new neural connections and strengthening existing ones.

This discovery has profound implications for education and rehabilitation. Adults learning a second language, for instance, show measurable changes in brain structure, with increased gray matter in language-processing regions. Similarly, stroke patients who engage in intensive therapy can sometimes regain lost functions as undamaged parts of the brain take over the roles of damaged areas. The brain's ability to reorganize itself isn't unlimited—age, severity of injury, and other factors play important roles—but the potential for change extends far beyond what was previously thought possible.

Questions:
1. According to the passage, what was the traditional scientific view of brain structure, and how has this view changed?
2. What evidence does the passage provide to support the concept of neuroplasticity? Give specific examples.
3. What limitation of neuroplasticity is mentioned in the passage?""",
        expected_output_characteristics="A comprehensive answer that accurately addresses all three questions, draws information directly from the passage, distinguishes between what the passage states explicitly and what it implies, provides specific examples mentioned in the text, and demonstrates clear understanding of the main concepts without adding information not present in the passage.",
        development_examples=[
            TaskExample(
                input="""Passage: Marie Curie was the first woman to win a Nobel Prize and remains the only person to win Nobel Prizes in two different scientific fields—physics in 1903 and chemistry in 1911. Born in Warsaw in 1867, she moved to Paris to study at the Sorbonne, where she met her husband Pierre Curie. Together, they discovered two new elements: polonium and radium. Despite facing discrimination as a woman in science, her work on radioactivity laid the foundation for important medical treatments.

Question: What makes Marie Curie's Nobel Prize achievements unique?""",
                output="""Marie Curie's Nobel Prize achievements are unique in two ways, according to the passage:

1. She was the first woman to win a Nobel Prize
2. She is the only person to have won Nobel Prizes in two different scientific fields—she won in physics (1903) and chemistry (1911)

The passage specifically emphasizes that no other person has achieved this dual-field accomplishment, making her achievement historically singular.""",
                explanation="This answer accurately extracts the two key facts from the passage, provides specific details (years and fields), and stays grounded in what the text actually states without adding outside information."
            ),
            TaskExample(
                input="""Passage: The Mediterranean diet, rich in olive oil, fish, vegetables, and whole grains, has been associated with numerous health benefits in scientific studies. Researchers attribute these benefits primarily to the diet's high content of omega-3 fatty acids from fish and monounsaturated fats from olive oil, rather than to any single "superfood."

Question: According to the passage, what causes the health benefits of the Mediterranean diet?""",
                output="""According to the passage, researchers attribute the health benefits of the Mediterranean diet primarily to two nutritional components:

1. Omega-3 fatty acids, which come from fish
2. Monounsaturated fats, which come from olive oil

The passage specifically notes that these benefits are due to these nutritional components rather than any single "superfood," suggesting it's the combination and type of fats that matter.""",
                explanation="This answer correctly identifies the specific causal factors mentioned in the passage and notes the distinction the passage makes about the source of benefits."
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
        },
        is_complete=True
    )
