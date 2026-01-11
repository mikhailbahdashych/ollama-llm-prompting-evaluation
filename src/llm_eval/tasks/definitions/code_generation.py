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
        description="This task evaluates the model's ability to write correct, efficient, and well-documented Python code that solves a specific algorithmic problem.",
        evaluation_input="""Write a Python function called `find_pair_sum` that takes a list of integers and a target sum as parameters. The function should return all unique pairs of numbers from the list that add up to the target sum.

Requirements:
- Function signature: `def find_pair_sum(numbers: list[int], target: int) -> list[tuple[int, int]]`
- Each pair should be returned as a tuple with the smaller number first
- Pairs should be unique (no duplicate pairs)
- Return an empty list if no pairs are found
- The same element cannot be used twice in a pair

Example:
- Input: numbers = [2, 7, 11, 15, 3], target = 9
- Output: [(2, 7)]

- Input: numbers = [1, 5, 3, 7, 2, 8], target = 10
- Output: [(2, 8), (3, 7)]

Write the complete function with appropriate documentation.""",
        expected_output_characteristics="A complete, working Python function with a docstring that explains parameters and return value. The solution should handle edge cases (empty list, no pairs found) and use an efficient algorithm (preferably O(n) time complexity using a set or dictionary). Code should be clean and readable with meaningful variable names.",
        development_examples=[
            TaskExample(
                input="Write a Python function called `reverse_string` that takes a string and returns it reversed. Include a docstring.",
                output="""def reverse_string(text: str) -> str:
    \"\"\"
    Reverse the input string.

    Args:
        text: The string to reverse

    Returns:
        The reversed string
    \"\"\"
    return text[::-1]""",
                explanation="This solution is clean and uses Python's slice notation efficiently. It includes a proper docstring documenting the function's purpose, parameters, and return value."
            ),
            TaskExample(
                input="Write a Python function called `is_prime` that checks if a number is prime. The function should return True if the number is prime, False otherwise.",
                output="""def is_prime(n: int) -> bool:
    \"\"\"
    Check if a number is prime.

    Args:
        n: The number to check

    Returns:
        True if n is prime, False otherwise
    \"\"\"
    if n < 2:
        return False

    # Check divisibility up to square root of n
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False

    return True"""
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
        },
        is_complete=True
    )
