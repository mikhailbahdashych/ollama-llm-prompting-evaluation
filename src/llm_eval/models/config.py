"""Model configurations for LLM evaluation."""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ModelConfig:
    """Configuration for an LLM model.

    Attributes:
        name: Ollama model name (e.g., "qwen2.5:1.5b")
        display_name: Human-readable name for reports
        size_category: Either "small" or "large"
        is_reasoning_model: True if model has built-in reasoning (e.g., DeepSeek-R1)
        parameters: Parameter count as string (e.g., "1.5B", "7B")
        supported_strategies: List of prompting strategies to use with this model
        temperature: Temperature parameter for generation (0.0-1.0)
        top_p: Top-p sampling parameter
        max_tokens: Maximum tokens to generate
        additional_params: Optional additional Ollama parameters
    """
    name: str
    display_name: str
    size_category: str  # "small" or "large"
    is_reasoning_model: bool
    parameters: str
    supported_strategies: List[str]
    temperature: float = 0.7
    top_p: float = 0.9
    max_tokens: int = 2048
    additional_params: Dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "display_name": self.display_name,
            "size_category": self.size_category,
            "is_reasoning_model": self.is_reasoning_model,
            "parameters": self.parameters,
            "supported_strategies": self.supported_strategies,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
            "additional_params": self.additional_params
        }


# Model registry with the two selected models
MODELS: Dict[str, ModelConfig] = {
    "small": ModelConfig(
        name="qwen2.5:1.5b",
        display_name="Qwen 2.5 (1.5B)",
        size_category="small",
        is_reasoning_model=False,
        parameters="1.5B",
        supported_strategies=["zero_shot", "few_shot", "chain_of_thought"],
        max_tokens=-1  # Unlimited tokens - let the model generate full response
    ),
    "large": ModelConfig(
        name="deepseek-r1:7b",
        display_name="DeepSeek R1 (7B)",
        size_category="large",
        is_reasoning_model=True,
        parameters="7B",
        supported_strategies=["zero_shot", "few_shot"],  # No CoT - it's a reasoning model
        max_tokens=-1  # Unlimited tokens - let the model generate full response
    )
}


def get_model(model_key: str) -> ModelConfig:
    """Get model configuration by key.

    Args:
        model_key: Either "small" or "large"

    Returns:
        ModelConfig for the requested model

    Raises:
        KeyError: If model_key is not found
    """
    if model_key not in MODELS:
        raise KeyError(f"Model '{model_key}' not found. Available models: {list(MODELS.keys())}")
    return MODELS[model_key]


def get_all_models() -> List[ModelConfig]:
    """Get all configured models.

    Returns:
        List of all ModelConfig objects
    """
    return list(MODELS.values())


def get_models_by_category(category: str) -> List[ModelConfig]:
    """Get all models in a specific size category.

    Args:
        category: Either "small" or "large"

    Returns:
        List of ModelConfig objects matching the category
    """
    return [model for model in MODELS.values() if model.size_category == category]
