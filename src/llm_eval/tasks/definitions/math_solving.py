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
        description="This task evaluates the model's ability to solve mathematical problems using appropriate methods, show clear step-by-step work, explain mathematical reasoning, and arrive at correct numerical answers.",
        evaluation_input="""Solve the following math problems. Show all your work and explain your reasoning for each step.

Problem 1: Sarah is planning a rectangular garden. The length is 3 meters more than twice the width. If the perimeter of the garden is 36 meters, what are the dimensions (length and width) of the garden?

Problem 2: A store is having a sale. A jacket originally costs $120. First, it's discounted by 25%, and then an additional 10% is taken off the sale price. What is the final price of the jacket?

Problem 3: If f(x) = 2x² - 5x + 3, find f(4). Show your substitution and calculation steps.

Solve all three problems with clear step-by-step work.""",
        expected_output_characteristics="Solutions that show complete mathematical work with each step clearly explained, use appropriate mathematical notation and terminology, apply correct methods (setting up equations, proper order of operations, correct algebraic manipulation), arrive at correct numerical answers, and include units where appropriate. The work should be organized and easy to follow.",
        development_examples=[
            TaskExample(
                input="""Problem: Tom has $500 in a savings account that earns 4% simple interest per year. How much money will he have after 3 years? Show your work.""",
                output="""To solve this problem, I'll use the simple interest formula:

Simple Interest = Principal × Rate × Time
Final Amount = Principal + Simple Interest

Given information:
- Principal (P) = $500
- Rate (R) = 4% = 0.04 (converting percentage to decimal)
- Time (T) = 3 years

Step 1: Calculate the simple interest
Simple Interest = P × R × T
Simple Interest = $500 × 0.04 × 3
Simple Interest = $60

Step 2: Calculate the final amount
Final Amount = Principal + Simple Interest
Final Amount = $500 + $60
Final Amount = $560

Answer: Tom will have $560 after 3 years.""",
                explanation="This solution shows clear organization, identifies the appropriate formula, lists given information, shows each calculation step, and provides the final answer with appropriate units (dollars)."
            ),
            TaskExample(
                input="""Problem: Solve for x: 3(x - 4) = 2x + 5""",
                output="""I'll solve this equation step by step using algebraic manipulation.

Starting equation: 3(x - 4) = 2x + 5

Step 1: Distribute the 3 on the left side
3x - 12 = 2x + 5

Step 2: Subtract 2x from both sides to get x terms on one side
3x - 2x - 12 = 2x - 2x + 5
x - 12 = 5

Step 3: Add 12 to both sides to isolate x
x - 12 + 12 = 5 + 12
x = 17

Step 4: Check the solution by substituting back
Left side: 3(17 - 4) = 3(13) = 39
Right side: 2(17) + 5 = 34 + 5 = 39
Both sides equal 39 ✓

Answer: x = 17""",
                explanation="This shows proper algebraic technique with clear steps, explains each operation, and includes verification of the answer, demonstrating thorough mathematical problem-solving."
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
        is_complete=True
    )
