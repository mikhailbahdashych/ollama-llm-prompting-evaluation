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
        description="This task evaluates the model's ability to apply everyday knowledge, practical reasoning, and common sense understanding of how the physical and social world works to solve realistic problems.",
        evaluation_input="""Answer the following common sense reasoning questions. Explain your reasoning for each answer.

1. Sarah left her ice cream on the kitchen counter and went to her room for 2 hours on a hot summer day. When she came back, what most likely happened to the ice cream? Why?

2. Tom wants to hang a heavy picture frame on his wall. He has: a hammer, nails, tape, and glue. Which tool(s) should he use and why? What would happen if he used the wrong tool?

3. Lisa is running late for an important meeting across town. She sees two routes: one is shorter (15 minutes) but goes through the city center during rush hour, the other is longer (25 minutes) but uses the highway. Which route should she choose and why? Consider what factors matter in this decision.

Provide your answers with clear common sense reasoning.""",
        expected_output_characteristics="Answers that demonstrate practical, real-world understanding of physical laws (ice cream melts), appropriate use of tools (nails and hammer for heavy items), and consideration of realistic factors in decision-making (traffic patterns affect travel time). The reasoning should be grounded in everyday experience and show understanding of cause-and-effect relationships in common situations.",
        development_examples=[
            TaskExample(
                input="""Question: You need to know if milk in your refrigerator is still good to drink. The expiration date was 3 days ago. What should you do before drinking it?""",
                output="""Before drinking the milk, you should:

1. Smell it - sour milk has a distinct unpleasant odor
2. Check its appearance - look for any discoloration or lumps
3. If it passes those tests, taste a small amount

This is common sense because even though the expiration date was 3 days ago, milk can still be good if properly refrigerated, or it might have gone bad before the date if not stored correctly. The expiration date is a guideline, but your senses (smell, sight, taste) are reliable indicators of whether food is safe. Most people have learned through experience that sour milk smells and tastes bad, so checking before consuming is a practical safety measure.""",
                explanation="This demonstrates common sense by combining knowledge of expiration dates (they're guidelines, not absolutes), understanding of food safety, and practical testing methods that anyone can perform."
            ),
            TaskExample(
                input="""Question: Why do people typically check the weather forecast before planning an outdoor wedding?""",
                output="""People check the weather forecast before planning an outdoor wedding because:

1. Rain or storms would ruin an outdoor event, making guests uncomfortable and damaging decorations
2. Extreme heat or cold affects guest comfort and safety
3. Weather can't be controlled, but planning can be adjusted based on forecasts
4. Having a backup plan (like a tent or indoor location) requires advance preparation

This is common sense because outdoor events are directly affected by weather conditions, and checking the forecast allows people to either choose a better date or prepare contingencies. It's much easier to prevent weather-related problems than to deal with them during the event. Most people have experienced being caught in unexpected rain and understand why advance planning matters.""",
                explanation="This shows understanding of practical planning, cause-and-effect (weather affects outdoor activities), and why prevention is better than reaction in event planning."
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
        },
        is_complete=True
    )
