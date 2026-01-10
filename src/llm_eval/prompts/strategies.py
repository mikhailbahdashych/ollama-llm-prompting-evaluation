"""Prompting strategies for LLM evaluation."""

from abc import ABC, abstractmethod
from typing import List

from ..tasks.base import Task, TaskExample


class PromptStrategy(ABC):
    """Abstract base class for prompting strategies."""

    @abstractmethod
    def build_prompt(self, task: Task, **kwargs) -> str:
        """Build a prompt for the given task.

        Args:
            task: The Task object containing evaluation content
            **kwargs: Additional strategy-specific parameters

        Returns:
            The formatted prompt string
        """
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Get the name of this strategy.

        Returns:
            Strategy name (e.g., "zero_shot", "few_shot", "chain_of_thought")
        """
        pass


class ZeroShotStrategy(PromptStrategy):
    """Zero-shot prompting: just the task, no examples.

    This strategy provides only the task description and evaluation input
    without any examples or additional guidance.
    """

    def build_prompt(self, task: Task, **kwargs) -> str:
        """Build a zero-shot prompt.

        Args:
            task: The Task object

        Returns:
            Prompt with just task description and input
        """
        return f"""{task.description}

{task.evaluation_input}"""

    def get_strategy_name(self) -> str:
        """Get strategy name."""
        return "zero_shot"


class FewShotStrategy(PromptStrategy):
    """Few-shot prompting: includes 2-3 examples before the task.

    This strategy provides example inputs and outputs to guide the model
    before presenting the actual evaluation task.
    """

    def build_prompt(self, task: Task, num_examples: int = 2, **kwargs) -> str:
        """Build a few-shot prompt with examples.

        Args:
            task: The Task object
            num_examples: Number of examples to include (default: 2)

        Returns:
            Prompt with examples followed by the actual task
        """
        if not task.development_examples:
            # Fallback to zero-shot if no examples available
            return ZeroShotStrategy().build_prompt(task)

        # Limit to available examples
        num_examples = min(num_examples, len(task.development_examples))
        examples = task.development_examples[:num_examples]

        # Build examples section
        examples_text = "Here are some examples:\n\n"
        for i, example in enumerate(examples, 1):
            examples_text += f"Example {i}:\n"
            examples_text += f"Input: {example.input}\n"
            examples_text += f"Output: {example.output}\n"
            if example.explanation:
                examples_text += f"Explanation: {example.explanation}\n"
            examples_text += "\n"

        # Combine with actual task
        return f"""{task.description}

{examples_text}Now solve this:
{task.evaluation_input}"""

    def get_strategy_name(self) -> str:
        """Get strategy name."""
        return "few_shot"


class ChainOfThoughtStrategy(PromptStrategy):
    """Chain-of-Thought prompting: explicitly request step-by-step thinking.

    This strategy adds explicit instructions to think through the problem
    step by step before providing the final answer. Only use with standard
    models, NOT with reasoning models like DeepSeek-R1.
    """

    def build_prompt(self, task: Task, **kwargs) -> str:
        """Build a chain-of-thought prompt.

        Args:
            task: The Task object

        Returns:
            Prompt with step-by-step reasoning instructions
        """
        return f"""{task.description}

{task.evaluation_input}

Let's approach this step by step:
1. First, analyze the problem carefully
2. Then, work through it systematically
3. Finally, provide your answer

Please show your reasoning at each step."""

    def get_strategy_name(self) -> str:
        """Get strategy name."""
        return "chain_of_thought"


# Strategy registry for easy access
STRATEGIES = {
    "zero_shot": ZeroShotStrategy(),
    "few_shot": FewShotStrategy(),
    "chain_of_thought": ChainOfThoughtStrategy()
}


def get_strategy(strategy_name: str) -> PromptStrategy:
    """Get a prompting strategy by name.

    Args:
        strategy_name: Name of the strategy ("zero_shot", "few_shot", "chain_of_thought")

    Returns:
        The corresponding PromptStrategy instance

    Raises:
        KeyError: If strategy name is not recognized
    """
    if strategy_name not in STRATEGIES:
        raise KeyError(
            f"Strategy '{strategy_name}' not found. "
            f"Available strategies: {list(STRATEGIES.keys())}"
        )
    return STRATEGIES[strategy_name]


def get_all_strategies() -> List[PromptStrategy]:
    """Get all available prompting strategies.

    Returns:
        List of all PromptStrategy instances
    """
    return list(STRATEGIES.values())
