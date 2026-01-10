# LLM Evaluation System with Diverse Prompting Strategies

A systematic evaluation framework for comparing Large Language Models across multiple task types using different prompting strategies.

## Overview

This project evaluates two LLMs (one small 1.5B, one large 7B) across 10 diverse task categories using zero-shot, few-shot, and chain-of-thought prompting strategies. The system uses Ollama for local model execution and produces structured JSON results for analysis.

### Models

- **Small Model**: Qwen 2.5 (1.5B parameters)
  - Strategies: zero-shot, few-shot, chain-of-thought
- **Large Model**: DeepSeek R1 (7B parameters, reasoning-focused)
  - Strategies: zero-shot, few-shot (no CoT as it's a reasoning model)

### Evaluation Tasks (10 Categories)

1. Instruction Following
2. Logical Reasoning
3. Creative Writing
4. Code Generation
5. Reading Comprehension
6. Common Sense Reasoning
7. Language Understanding & Ambiguity
8. Factual Knowledge & Retrieval
9. Mathematical Problem Solving
10. Ethical Reasoning & Nuance

**Total Evaluations**: 50 (10 tasks × 5 strategy combinations)

## Prerequisites

- Python 3.12 or higher
- Ollama installed and running locally
- At least 8GB RAM (16GB+ recommended for larger models)

## Installation

### 1. Install Ollama

Visit [ollama.com](https://ollama.com) and follow the installation instructions for your platform.

### 2. Pull Required Models

```bash
# Pull the small model (Qwen 2.5 1.5B)
ollama pull qwen2.5:1.5b

# Pull the large reasoning model (DeepSeek R1 7B)
ollama pull deepseek-r1:7b

# Verify models are available
ollama list
```

### 3. Install Project Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

## Project Structure

```
.
├── src/llm_eval/              # Main package
│   ├── tasks/                 # Task definitions
│   │   ├── base.py           # Base Task and TaskExample classes
│   │   ├── registry.py       # Task registry and loader
│   │   └── definitions/      # 10 task definition files
│   ├── models/               # Model configurations
│   │   ├── config.py         # Model registry (MODELS)
│   │   └── ollama_client.py  # Ollama HTTP API client
│   ├── prompts/              # Prompting strategies
│   │   ├── strategies.py     # ZeroShot, FewShot, ChainOfThought
│   │   └── builders.py       # Prompt formatting utilities
│   ├── evaluation/           # Evaluation engine
│   │   └── evaluator.py      # Main orchestrator
│   └── results/              # Results management
│       └── storage.py        # JSON persistence and reporting
├── data/
│   ├── examples/             # Development examples (future)
│   └── results/              # Evaluation outputs
│       ├── raw/              # Raw model responses
│       ├── scored/           # Scored evaluations
│       └── reports/          # Summary reports
├── scripts/
│   └── run_evaluation.py     # Main execution script
└── main.py                   # Entry point wrapper

```

## Usage

### Quick Start

```bash
# Run all evaluations (50 total)
python scripts/run_evaluation.py

# Or use the main.py wrapper
python main.py
```

### Command Line Options

#### List Available Tasks

```bash
python scripts/run_evaluation.py --list-tasks
```

Output shows all 10 tasks with their completion status (tasks with TODO markers are marked as incomplete).

#### List Configured Models

```bash
python scripts/run_evaluation.py --list-models
```

Shows model details, parameters, and supported strategies.

#### Validate Task Definitions

```bash
python scripts/run_evaluation.py --validate-tasks
```

Reports which task fields still have TODO placeholders that need to be filled in.

#### Run Specific Tasks

```bash
# Run only specific tasks
python scripts/run_evaluation.py --tasks logical_reasoning,math_solving

# Run only with the small model
python scripts/run_evaluation.py --models small

# Run only with the large model
python scripts/run_evaluation.py --models large
```

#### Advanced Options

```bash
# Use custom Ollama URL
python scripts/run_evaluation.py --ollama-url http://localhost:11434

# Custom results directory
python scripts/run_evaluation.py --results-dir /path/to/results

# Enable verbose logging
python scripts/run_evaluation.py --verbose

# Skip Ollama connection validation
python scripts/run_evaluation.py --skip-validation
```

### Full Command Reference

```
usage: run_evaluation.py [-h] [--tasks TASKS] [--models MODELS]
                         [--ollama-url OLLAMA_URL] [--results-dir RESULTS_DIR]
                         [--verbose] [--skip-validation] [--list-tasks]
                         [--list-models] [--validate-tasks]

Options:
  --tasks TASKS              Comma-separated task IDs to run (default: all)
  --models MODELS            Comma-separated model keys (default: all)
  --ollama-url OLLAMA_URL    Ollama API URL (default: http://localhost:11434)
  --results-dir RESULTS_DIR  Results directory (default: data/results)
  --verbose, -v              Enable verbose logging
  --skip-validation          Skip Ollama connection check
  --list-tasks               List all available tasks and exit
  --list-models              List all configured models and exit
  --validate-tasks           Validate task definitions and exit
```

## Filling in Task Definitions

Currently, all task definition files contain TODO placeholders. To complete the tasks:

1. Navigate to `src/llm_eval/tasks/definitions/`
2. Edit each task file (e.g., `logical_reasoning.py`)
3. Replace all `[TODO: ...]` markers with actual content:
   - `description`: What the task tests
   - `evaluation_input`: The actual problem to solve
   - `expected_output_characteristics`: What good output looks like
   - `development_examples`: 2-3 example inputs/outputs for few-shot prompting

### Example: Completing a Task

Before:
```python
evaluation_input="[TODO: Add actual logical reasoning problem]"
```

After:
```python
evaluation_input="If all roses are flowers, and some flowers fade quickly, can we conclude that some roses fade quickly? Explain your reasoning."
```

### Validation

Check which tasks are complete:
```bash
python scripts/run_evaluation.py --validate-tasks
```

## Results

### Directory Structure

After running evaluations, results are organized as:

```
data/results/
└── run_YYYY-MM-DD_HH-MM-SS/
    ├── raw/
    │   ├── instruction_following_qwen2.5_1.5b_zero_shot.json
    │   ├── instruction_following_qwen2.5_1.5b_few_shot.json
    │   ├── instruction_following_qwen2.5_1.5b_chain_of_thought.json
    │   ├── instruction_following_deepseek-r1_7b_zero_shot.json
    │   ├── instruction_following_deepseek-r1_7b_few_shot.json
    │   └── ... (45 more files)
    └── reports/
        ├── run_YYYY-MM-DD_HH-MM-SS_summary.json
        └── run_YYYY-MM-DD_HH-MM-SS_results.csv
```

### Result File Format

Each JSON file contains:

```json
{
  "task_id": "logical_reasoning",
  "model_name": "qwen2.5:1.5b",
  "strategy": "zero_shot",
  "prompt": "Full prompt sent to the model...",
  "response": "Model's response...",
  "timestamp": "2026-01-10T16:30:45.123456",
  "model_config": {...},
  "generation_time_ms": 1234,
  "prompt_tokens": 45,
  "completion_tokens": 123,
  "scores": null,
  "total_score": null,
  "evaluator_notes": null
}
```

### Manual Scoring

After generating results, manually score each evaluation:

1. Open a result JSON file
2. Read the `prompt` and `response`
3. Score based on the task's `scoring_rubric`
4. Add scores to the JSON:
   ```json
   "scores": {
     "logical_validity": 8,
     "completeness": 4,
     "clarity": 5
   },
   "total_score": 17,
   "evaluator_notes": "Good logical structure but missed one edge case."
   ```

## Architecture

### Core Components

1. **Task System** (`src/llm_eval/tasks/`)
   - `Task` and `TaskExample` dataclasses for type-safe task definitions
   - `TaskRegistry` for loading and managing all tasks
   - Individual task definition files in `definitions/`

2. **Model Management** (`src/llm_eval/models/`)
   - `ModelConfig` dataclass for model metadata
   - `OllamaClient` for HTTP API communication
   - `MODELS` registry with configured models

3. **Prompting Strategies** (`src/llm_eval/prompts/`)
   - Abstract `PromptStrategy` base class
   - `ZeroShotStrategy`: Task only, no examples
   - `FewShotStrategy`: Includes 2-3 examples
   - `ChainOfThoughtStrategy`: Adds step-by-step reasoning

4. **Evaluation Engine** (`src/llm_eval/evaluation/`)
   - `Evaluator`: Orchestrates the complete evaluation pipeline
   - Handles task-model-strategy combinations
   - Progress tracking with Rich library
   - Error handling and retry logic

5. **Results Management** (`src/llm_eval/results/`)
   - `EvaluationResult` dataclass for results
   - `ResultsStorage` for JSON persistence
   - CSV export and summary report generation

### Execution Flow

```
1. Load tasks from TaskRegistry → 10 tasks
2. Load models from MODELS → 2 models
3. Build evaluation matrix:
   - Small model × 10 tasks × 3 strategies = 30 evals
   - Large model × 10 tasks × 2 strategies = 20 evals
   - Total = 50 evaluations
4. For each evaluation:
   a. Get strategy → build prompt
   b. Call Ollama → generate response
   c. Save result as JSON
5. Generate summary report
```

## Troubleshooting

### Ollama Connection Issues

**Error**: "Could not connect to Ollama"

**Solution**:
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start Ollama
ollama serve
```

### Model Not Found

**Error**: Model not available in Ollama

**Solution**:
```bash
# List available models
ollama list

# Pull missing model
ollama pull qwen2.5:1.5b
ollama pull deepseek-r1:7b
```

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'llm_eval'`

**Solution**:
```bash
# Ensure you're running from project root
cd /path/to/LAB5\ 08.01.2026

# Reinstall dependencies
uv sync
```

### Memory Issues

**Error**: Out of memory or slow generation

**Solution**:
- Close other applications
- Use smaller models
- Reduce max_tokens in `src/llm_eval/models/config.py`

## Development

### Adding a New Task

1. Create a new file in `src/llm_eval/tasks/definitions/`:
   ```python
   # src/llm_eval/tasks/definitions/my_new_task.py
   from ..base import Task, TaskExample

   def create_my_new_task() -> Task:
       return Task(
           id="my_new_task",
           name="My New Task",
           # ... fill in all fields
       )
   ```

2. Import in `src/llm_eval/tasks/registry.py`:
   ```python
   from .definitions.my_new_task import create_my_new_task

   # Add to task_creators list
   task_creators = [
       # ... existing tasks
       create_my_new_task
   ]
   ```

### Adding a New Model

Edit `src/llm_eval/models/config.py`:

```python
MODELS = {
    # ... existing models
    "new_model": ModelConfig(
        name="model-name:tag",
        display_name="Model Display Name",
        size_category="small",  # or "large"
        is_reasoning_model=False,
        parameters="3B",
        supported_strategies=["zero_shot", "few_shot", "chain_of_thought"]
    )
}
```

### Adding a New Prompting Strategy

1. Create a new class in `src/llm_eval/prompts/strategies.py`:
   ```python
   class MyNewStrategy(PromptStrategy):
       def build_prompt(self, task: Task, **kwargs) -> str:
           # Your prompt building logic
           pass

       def get_strategy_name(self) -> str:
           return "my_new_strategy"
   ```

2. Register in the `STRATEGIES` dictionary:
   ```python
   STRATEGIES = {
       # ... existing strategies
       "my_new_strategy": MyNewStrategy()
   }
   ```

## License

This is a university laboratory assignment. All rights reserved.

## Acknowledgments

- Assignment provided by the Language and Ontology course
- Models hosted via [Ollama](https://ollama.com)
- Qwen models by Alibaba Cloud
- DeepSeek models by DeepSeek AI
