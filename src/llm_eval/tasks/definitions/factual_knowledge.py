"""Factual Knowledge & Retrieval task definition."""

from ..base import Task, TaskExample


def create_factual_knowledge_task() -> Task:
    """Create the Factual Knowledge & Retrieval evaluation task.

    This task evaluates the model's ability to recall and apply
    factual information accurately.
    """
    return Task(
        id="factual_knowledge",
        name="Factual Knowledge & Retrieval",
        category="Knowledge",
        description="This task evaluates the model's ability to accurately recall factual information, provide specific and verifiable details, and demonstrate knowledge across different domains while distinguishing between certainty and uncertainty.",
        evaluation_input="""Answer the following factual questions with accurate, specific information. If you are uncertain about any part of an answer, indicate this.

1. What is the speed of light in a vacuum, and why is this value significant in physics? Provide the value with appropriate units.

2. Who wrote the novel "One Hundred Years of Solitude," and in what year was it originally published? What literary movement is this author associated with?

3. What is photosynthesis, and what are the main inputs and outputs of this process? Include the basic chemical equation if possible.

4. Name three countries that share a border with Germany and provide their capital cities.

Provide accurate, specific factual information for each question.""",
        expected_output_characteristics="Answers that provide accurate, specific, and verifiable facts with appropriate details (numbers with units, dates, names spelled correctly, specific locations). The response should demonstrate confident knowledge on factual matters, include relevant context that shows understanding beyond mere memorization, and honestly acknowledge if certain details are uncertain rather than guessing.",
        development_examples=[
            TaskExample(
                input="""Question: What is the capital of Australia, and why do people often incorrectly think it's Sydney?""",
                output="""The capital of Australia is Canberra, not Sydney.

Canberra was purpose-built as the capital and officially became the capital in 1913. It's located in the Australian Capital Territory (ACT), which was created specifically to house the nation's capital.

People often incorrectly think Sydney is the capital because:
1. Sydney is Australia's largest and most internationally well-known city
2. Sydney is the capital of New South Wales, the most populous state
3. Sydney is a major cultural and economic hub with iconic landmarks (Opera House, Harbour Bridge)
4. Many countries have their largest city as the capital, leading to this assumption

However, similar to Washington D.C. in the United States or Brasília in Brazil, Australia chose to create a planned capital city in a neutral location between the rival cities of Sydney and Melbourne.""",
                explanation="This provides the correct factual answer with specific details, explains the historical context, and addresses why the misconception exists, showing deeper knowledge beyond just naming the capital."
            ),
            TaskExample(
                input="""Question: How many planets are in our solar system, and has this number changed?""",
                output="""There are currently 8 recognized planets in our solar system: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, and Neptune (in order from the Sun).

This number did change in 2006. Previously, there were 9 planets, including Pluto. However, in August 2006, the International Astronomical Union (IAU) redefined what constitutes a planet. Under the new definition, a celestial body must:
1. Orbit the Sun
2. Have sufficient mass for self-gravity to make it round
3. Have "cleared the neighborhood" around its orbit

Pluto failed the third criterion because its orbit overlaps with other objects in the Kuiper Belt. It was reclassified as a "dwarf planet," along with Eris, Makemake, Haumea, and Ceres.

So the answer changed from 9 to 8 planets, not because we discovered Pluto wasn't there, but because we refined our definition of what a planet is.""",
                explanation="This provides the accurate current number, explains the historical change, gives specific details about when and why the change occurred, and demonstrates understanding of the scientific reasoning behind the reclassification."
            )
        ],
        evaluation_criteria={
            "accuracy": "Information is factually correct",
            "completeness": "Answer includes relevant details",
            "specificity": "Provides specific, not vague information",
            "source_reliability": "Information comes from reliable knowledge"
        },
        scoring_rubric={
            "accuracy": 10,
            "completeness": 5,
            "specificity": 3,
            "source_reliability": 2
        },
        is_complete=True
    )
