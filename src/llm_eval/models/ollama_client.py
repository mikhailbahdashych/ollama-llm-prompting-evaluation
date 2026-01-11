"""Ollama HTTP API client for LLM interaction."""

import json
import logging
from typing import Any, Dict, Optional

import requests


logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for interacting with Ollama HTTP API.

    This client provides methods to generate text using Ollama models
    running locally on the default port (11434).
    """

    def __init__(self, base_url: str = "http://localhost:11434"):
        """Initialize Ollama client.

        Args:
            base_url: Base URL for Ollama API (default: http://localhost:11434)
        """
        self.base_url = base_url.rstrip("/")
        self.generate_endpoint = f"{self.base_url}/api/generate"
        self.tags_endpoint = f"{self.base_url}/api/tags"

    def generate(
        self,
        model: str,
        prompt: str,
        temperature: float = 0.7,
        top_p: float = 0.9,
        max_tokens: int = 2048,
        stream: bool = False,
        timeout: int = 600
    ) -> Dict[str, Any]:
        """Generate text using an Ollama model.

        Args:
            model: Model name (e.g., "qwen2.5:1.5b", "deepseek-r1:7b")
            prompt: The prompt text to send to the model
            temperature: Sampling temperature (0.0-1.0)
            top_p: Top-p sampling parameter (0.0-1.0)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response (default: False)
            timeout: Request timeout in seconds (default: 600)

        Returns:
            Dict containing:
                - response: The generated text
                - model: Model name used
                - created_at: Timestamp
                - done: Whether generation is complete
                - context: Context window used
                - total_duration: Total time in nanoseconds
                - load_duration: Model load time in nanoseconds
                - prompt_eval_count: Number of tokens in prompt
                - eval_count: Number of tokens generated

        Raises:
            requests.exceptions.RequestException: If the API call fails
            ValueError: If the response is invalid
        """
        # Build options dict
        options = {
            "temperature": temperature,
            "top_p": top_p
        }

        # Only add num_predict if it's not -1 (unlimited)
        # For unlimited generation, we omit the parameter entirely
        if max_tokens != -1:
            options["num_predict"] = max_tokens

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            "options": options
        }

        logger.info(f"Generating text with model: {model} (max_tokens: {max_tokens})")
        logger.debug(f"Prompt length: {len(prompt)} characters")

        try:
            response = requests.post(
                self.generate_endpoint,
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()

            result = response.json()

            if not result.get("done", False):
                logger.warning("Generation may not be complete (done=False)")

            # Check if response is empty
            response_text = result.get("response", "")
            if not response_text or response_text.strip() == "":
                logger.warning(
                    f"Empty response received from model {model}. "
                    f"Generated {result.get('eval_count', 0)} tokens but response field is empty. "
                    f"This may happen with reasoning models that hit token limits."
                )

            logger.info(f"Generation complete. Tokens: {result.get('eval_count', 0)}")
            return result

        except requests.exceptions.Timeout:
            logger.error(f"Request timeout after {timeout}s for model {model}")
            raise
        except requests.exceptions.ConnectionError:
            logger.error(
                f"Could not connect to Ollama at {self.base_url}. "
                "Make sure Ollama is running (try: ollama serve)"
            )
            raise
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error from Ollama API: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response from Ollama: {e}")
            raise ValueError(f"Invalid response from Ollama API: {e}")

    def check_model_availability(self, model: str) -> bool:
        """Check if a model is available in Ollama.

        Args:
            model: Model name to check

        Returns:
            True if model is available, False otherwise
        """
        try:
            response = requests.get(self.tags_endpoint, timeout=10)
            response.raise_for_status()
            data = response.json()

            available_models = [m.get("name", "") for m in data.get("models", [])]
            return model in available_models

        except Exception as e:
            logger.error(f"Error checking model availability: {e}")
            return False

    def list_models(self) -> list:
        """List all available models in Ollama.

        Returns:
            List of model names

        Raises:
            requests.exceptions.RequestException: If the API call fails
        """
        try:
            response = requests.get(self.tags_endpoint, timeout=10)
            response.raise_for_status()
            data = response.json()

            models = [m.get("name", "") for m in data.get("models", [])]
            logger.info(f"Found {len(models)} available models")
            return models

        except Exception as e:
            logger.error(f"Error listing models: {e}")
            raise

    def test_connection(self) -> bool:
        """Test connection to Ollama server.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = requests.get(self.tags_endpoint, timeout=5)
            response.raise_for_status()
            logger.info("Successfully connected to Ollama server")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {e}")
            return False
