"""Prompt building utilities and helpers."""

from typing import List, Optional

from ..tasks.base import TaskExample


def format_example(example: TaskExample, index: Optional[int] = None, include_explanation: bool = True) -> str:
    """Format a single example for use in prompts.

    Args:
        example: The TaskExample to format
        index: Optional index number for the example
        include_explanation: Whether to include the explanation field

    Returns:
        Formatted example string
    """
    parts = []

    if index is not None:
        parts.append(f"Example {index}:")

    parts.append(f"Input: {example.input}")
    parts.append(f"Output: {example.output}")

    if include_explanation and example.explanation:
        parts.append(f"Explanation: {example.explanation}")

    return "\n".join(parts)


def format_examples_section(examples: List[TaskExample], max_examples: int = 3) -> str:
    """Format multiple examples into a section for prompts.

    Args:
        examples: List of TaskExample objects
        max_examples: Maximum number of examples to include

    Returns:
        Formatted examples section
    """
    if not examples:
        return ""

    num_examples = min(len(examples), max_examples)
    selected_examples = examples[:num_examples]

    parts = ["Here are some examples:", ""]

    for i, example in enumerate(selected_examples, 1):
        parts.append(format_example(example, index=i, include_explanation=True))
        parts.append("")  # Empty line between examples

    return "\n".join(parts)


def add_step_by_step_instruction(base_prompt: str, num_steps: Optional[int] = None) -> str:
    """Add step-by-step reasoning instructions to a prompt.

    Args:
        base_prompt: The base prompt text
        num_steps: Optional specific number of steps to suggest

    Returns:
        Prompt with step-by-step instructions added
    """
    if num_steps:
        steps_text = f"Let's approach this step by step:\n"
        for i in range(1, num_steps + 1):
            steps_text += f"{i}. [Step {i}]\n"
        steps_text += "\nPlease work through each step carefully."
    else:
        steps_text = """Let's approach this step by step:
1. First, analyze the problem carefully
2. Then, work through it systematically
3. Finally, provide your answer

Please show your reasoning at each step."""

    return f"{base_prompt}\n\n{steps_text}"


def wrap_with_instructions(content: str, pre_instruction: str = "", post_instruction: str = "") -> str:
    """Wrap content with pre and post instructions.

    Args:
        content: The main content
        pre_instruction: Instruction to add before content
        post_instruction: Instruction to add after content

    Returns:
        Wrapped content
    """
    parts = []

    if pre_instruction:
        parts.append(pre_instruction)
        parts.append("")

    parts.append(content)

    if post_instruction:
        parts.append("")
        parts.append(post_instruction)

    return "\n".join(parts)


def truncate_prompt(prompt: str, max_length: int = 4000, suffix: str = "...") -> str:
    """Truncate a prompt to maximum length if needed.

    Args:
        prompt: The prompt to potentially truncate
        max_length: Maximum character length
        suffix: Suffix to add if truncated

    Returns:
        Truncated prompt if needed, otherwise original
    """
    if len(prompt) <= max_length:
        return prompt

    return prompt[:max_length - len(suffix)] + suffix
