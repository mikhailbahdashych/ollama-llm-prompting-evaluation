"""Logical Reasoning task definition."""

from ..base import Task, TaskExample


def create_logical_reasoning_task() -> Task:
    """Create the Logical Reasoning evaluation task.

    This task evaluates the model's ability to apply logical rules
    and derive valid conclusions.
    """
    return Task(
        id="logical_reasoning",
        name="Logical Reasoning",
        category="Reasoning",
        description="This task evaluates the model's ability to apply formal logical rules, identify valid and invalid inferences, and reason systematically from given premises to sound conclusions.",
        evaluation_input="""Consider the following premises:

1. All successful entrepreneurs take calculated risks.
2. Some people who take calculated risks fail in their ventures.
3. Maria is a successful entrepreneur.
4. Everyone who fails in their ventures learns valuable lessons.

Based on these premises, answer the following questions with logical reasoning:

a) Can we conclude that Maria takes calculated risks? Explain your reasoning.
b) Can we conclude that Maria has failed in her ventures? Explain why or why not.
c) If someone learns valuable lessons, does that necessarily mean they failed in their ventures? Explain the logical relationship.

Provide your analysis with clear logical reasoning for each answer.""",
        expected_output_characteristics="A response that demonstrates formal logical reasoning, correctly identifies what can and cannot be concluded from the premises, explains the logical relationships (e.g., 'all A are B' vs 'some A are B'), avoids logical fallacies (like affirming the consequent), and clearly distinguishes between necessary and possible conclusions.",
        development_examples=[
            TaskExample(
                input="""Given: All birds have feathers. Some animals with feathers can fly. Penguins are birds. Penguins cannot fly.

Question: What can we logically conclude about the relationship between having feathers and being able to fly?""",
                output="""We can conclude that having feathers is NOT sufficient for being able to fly. Here's the logical reasoning:

1. From "All birds have feathers" and "Penguins are birds," we know penguins have feathers.
2. From "Penguins cannot fly," we know that something can have feathers and not fly.
3. Therefore, having feathers does not guarantee the ability to fly.

The statement "Some animals with feathers can fly" tells us that flight is possible for some feathered animals, but the penguin example proves it's not universal. Having feathers is a necessary condition for birds, but not a sufficient condition for flight.""",
                explanation="This demonstrates proper logical reasoning by identifying the distinction between necessary and sufficient conditions, and correctly using the penguin counterexample to disprove a universal claim."
            ),
            TaskExample(
                input="""If it rains, the ground gets wet. The ground is wet. Can we conclude it rained?""",
                output="""No, we cannot logically conclude that it rained. This is a logical fallacy called "affirming the consequent."

The premise states: If rain → wet ground
We observe: wet ground
This does NOT allow us to conclude: rain

While rain is sufficient to make the ground wet, it's not the only possible cause. The ground could be wet from:
- Sprinklers
- A burst pipe
- Morning dew
- Someone washing their car

To validly conclude it rained, we would need the reverse implication: "If and only if it rains, the ground gets wet" or "The ground is wet only when it rains." Since we don't have this, we cannot make the conclusion.""",
                explanation="This correctly identifies the logical fallacy and explains why the reasoning is invalid, showing understanding of conditional logic and the difference between if-then and if-and-only-if relationships."
            )
        ],
        evaluation_criteria={
            "logical_validity": "Reasoning follows logical rules and principles",
            "completeness": "Addresses all aspects of the problem",
            "clarity": "Explanation is clear and well-structured"
        },
        scoring_rubric={
            "logical_validity": 10,
            "completeness": 5,
            "clarity": 5
        },
        is_complete=True
    )
