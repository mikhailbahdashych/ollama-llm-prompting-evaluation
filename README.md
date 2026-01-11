# LLM Evaluation System with Diverse Prompting Strategies

A systematic framework for evaluating and comparing Large Language Models (LLMs) across multiple task categories using different prompting strategies. This project provides a comprehensive toolkit for assessing model performance on tasks ranging from logical reasoning to creative writing, with support for zero-shot, few-shot, and chain-of-thought prompting techniques.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Architecture](#project-architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Evaluation Workflow](#evaluation-workflow)
  - [Step 1: Run Evaluations](#step-1-run-evaluations)
  - [Step 2: Manual Scoring](#step-2-manual-scoring)
  - [Step 3: Generate Reports](#step-3-generate-reports)
  - [Step 4: Generate Visualizations](#step-4-generate-visualizations)
- [Task Definitions](#task-definitions)
- [Prompting Strategies](#prompting-strategies)
- [Scripts Documentation](#scripts-documentation)
- [Directory Structure](#directory-structure)
- [Configuration](#configuration)
- [Results and Analysis](#results-and-analysis)
- [Extending the Framework](#extending-the-framework)
- [Requirements](#requirements)
- [Troubleshooting](#troubleshooting)

## Overview

This project implements a structured evaluation framework for comparing LLM performance across diverse cognitive tasks. The system is designed to answer key research questions about model capabilities:

- How does model size affect performance across different task types?
- Which prompting strategies are most effective for specific tasks?
- How do standard models compare to reasoning-specialized models?
- What are the performance-speed tradeoffs between different models?

The framework evaluates models on 10 distinct task categories, each with carefully designed evaluation criteria and development examples for few-shot prompting. All evaluations are conducted locally using Ollama, ensuring reproducibility and data privacy.

## Features

- **Comprehensive Task Coverage**: 10 evaluation tasks spanning logical reasoning, creative writing, code generation, reading comprehension, and more
- **Multiple Prompting Strategies**: Zero-shot, few-shot (2-3 examples), and chain-of-thought prompting
- **Flexible Model Support**: Compatible with any Ollama-supported model, with configurations for small (1-2B) and large (10-14B) models
- **Automated Evaluation Pipeline**: Streamlined workflow from model querying to result storage
- **Manual Scoring Framework**: Structured rubrics for human evaluation of model outputs
- **Rich Visualizations**: 10 different plot types for analyzing performance across models, tasks, and strategies
- **Extensible Architecture**: Modular design supporting easy addition of new tasks, models, or strategies

## Project Architecture

The system follows a modular architecture with clear separation of concerns:

```
src/llm_eval/
├── tasks/              # Task definitions and registry
│   ├── base.py        # Core data structures (Task, TaskExample)
│   ├── registry.py    # Task loading and management
│   └── definitions/   # Individual task implementations
├── prompts/           # Prompting strategy implementations
│   ├── strategies.py  # ZeroShot, FewShot, ChainOfThought classes
│   └── builders.py    # Prompt formatting utilities
├── models/            # Model configurations and API client
│   ├── config.py      # Model definitions and parameters
│   └── ollama_client.py  # Ollama HTTP API integration
├── evaluation/        # Evaluation orchestration
│   └── evaluator.py   # Main evaluation pipeline
└── results/           # Results management
    └── storage.py     # JSON persistence and CSV export
```

Each component is designed to be independently testable and extensible, facilitating both research experimentation and production deployment.

## Installation

### Prerequisites

- Python 3.12 or higher
- Ollama installed and running locally
- uv package manager (recommended) or pip

### Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd LAB5
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Install and configure Ollama:
```bash
# Install Ollama (macOS)
brew install ollama

# Start Ollama service
ollama serve
```

4. Pull required models:
```bash
# Small model (1-2B parameters)
ollama pull qwen2.5:1.5b

# Large reasoning model (7-14B parameters)
ollama pull deepseek-r1:7b

# Optional: other models
ollama pull ministral-3:3b
ollama pull qwen2.5:14b
```

5. Verify installation:
```bash
python scripts/run_evaluation.py --list-models
python scripts/run_evaluation.py --list-tasks
```

## Quick Start

Run a complete evaluation cycle:

```bash
# 1. Run all evaluations (generates JSON files)
python scripts/run_evaluation.py

# 2. Manually score the results by editing JSON files in data/results/raw/<run_id>/

# 3. Generate CSV report with calculated totals
python scripts/generate_report.py --latest

# 4. Create visualization plots
python scripts/generate_plots.py --latest
```

For selective evaluation:

```bash
# Run specific tasks only
python scripts/run_evaluation.py --tasks logical_reasoning,code_generation

# Run specific models only
python scripts/run_evaluation.py --models small

# Validate task completion status
python scripts/run_evaluation.py --validate-tasks
```

## Evaluation Workflow

The evaluation process follows a structured four-step workflow designed to separate automated model querying from human evaluation.

### Step 1: Run Evaluations

Execute the evaluation pipeline to query all models with all prompting strategies:

```bash
python scripts/run_evaluation.py
```

This command:
- Loads all complete tasks from the registry
- Builds an evaluation matrix (tasks x models x strategies)
- Queries each model via Ollama API
- Saves results as JSON files in `data/results/raw/<run_id>/`
- Creates companion markdown files (`*_res.md`) for easy result viewing
- Generates a summary report in `data/results/reports/`

**Output**: For each evaluation, two files are created:
- `{task}_{model}_{strategy}.json`: Complete evaluation data
- `{task}_{model}_{strategy}_res.md`: Model response only (for easy reading)

**Optional Parameters**:
- `--tasks <task_ids>`: Comma-separated list of specific tasks
- `--models <model_keys>`: Comma-separated list of model keys (e.g., "small,large")
- `--skip-validation`: Skip Ollama connection check
- `--verbose`: Enable debug logging

### Step 2: Manual Scoring

After evaluation, manually review and score each model's response:

1. Navigate to the run directory: `data/results/raw/<run_id>/`
2. For each JSON file, open and review the model's response
3. Fill in the `scores` field based on the task's scoring rubric
4. Optionally add `evaluator_notes` with observations

**Example Scoring** (for math_solving task):

```json
{
  "task_id": "math_solving",
  "model_name": "qwen2.5:1.5b",
  "strategy": "few_shot",
  "response": "...",
  "scores": {
    "correctness": 8,
    "methodology": 4,
    "step_clarity": 3,
    "explanation": 2
  },
  "evaluator_notes": "Good approach but minor arithmetic error in final step"
}
```

**Important**: Only fill in the `scores` dictionary. Do not manually calculate `total_score` - this will be computed automatically in Step 3.

**Scoring Guidelines**:
- Review the task definition in `src/llm_eval/tasks/definitions/<task_name>.py`
- Use the `scoring_rubric` to determine maximum points for each criterion
- Evaluate objectively based on `evaluation_criteria` descriptions
- Award partial credit where appropriate
- Document reasoning in `evaluator_notes` for transparency

### Step 3: Generate Reports

After scoring, generate the CSV report with calculated totals:

```bash
# Process a specific run
python scripts/generate_report.py run_2026-01-11_15-30-45

# Or process the most recent run
python scripts/generate_report.py --latest
```

This script:
- Reads all JSON files from the specified run
- Calculates `total_score` by summing values in the `scores` dictionary
- Updates JSON files with calculated totals
- Generates a CSV file in `data/results/reports/` for analysis

**Output**: `data/results/reports/<run_id>_results.csv` containing all evaluation data with scores.

### Step 4: Generate Visualizations

Create comprehensive plots for analysis:

```bash
# Generate plots from latest CSV
python scripts/generate_plots.py --latest

# Or specify a CSV file
python scripts/generate_plots.py data/results/reports/<run_id>_results.csv

# Specify output format
python scripts/generate_plots.py --latest --format pdf
```

This generates 10 visualization plots:

**Overall Performance**:
1. Total Score by Model - Average performance comparison
2. Performance by Task - Model comparison across tasks
3. Performance by Strategy - Prompting strategy effectiveness

**Model vs Task Analysis**:
4. Heatmap - Performance matrix with color coding
5. Score Distribution - Box plots showing variance
6. Generation Time - Response time comparison
7. Criteria Breakdown - Performance on specific evaluation criteria
8. Radar Chart - Circular visualization across all tasks
9. Task Winners - Individual plots showing best model per task
10. Model Specialization - Relative performance heatmap

**Output**: Plots saved to `data/results/reports/<run_id>_results_plots/`

## Task Definitions

The framework includes 10 diverse evaluation tasks, each designed to assess different cognitive capabilities:

### 1. Instruction Following
- **Category**: IFEval-style
- **Description**: Tests ability to follow multiple specific constraints simultaneously
- **Scoring**: Instruction adherence (10), completeness (5), format compliance (5)
- **Max Score**: 20 points

### 2. Logical Reasoning
- **Category**: Reasoning
- **Description**: Evaluates formal logic application and valid inference
- **Scoring**: Logical validity (10), completeness (5), clarity (5)
- **Max Score**: 20 points

### 3. Creative Writing
- **Category**: Generation
- **Description**: Assesses narrative creativity, coherence, and engagement
- **Scoring**: Creativity (5), coherence (5), engagement (5), language quality (5)
- **Max Score**: 20 points

### 4. Code Generation
- **Category**: Programming
- **Description**: Tests ability to write correct, efficient, documented code
- **Scoring**: Correctness (10), code quality (5), efficiency (3), documentation (2)
- **Max Score**: 20 points

### 5. Reading Comprehension
- **Category**: Understanding
- **Description**: Evaluates text understanding and information extraction
- **Scoring**: Accuracy (10), completeness (5), evidence-based (3), clarity (2)
- **Max Score**: 20 points

### 6. Common Sense Reasoning
- **Category**: Reasoning
- **Description**: Tests practical, real-world reasoning abilities
- **Scoring**: Practical reasoning (10), plausibility (5), explanation quality (5)
- **Max Score**: 20 points

### 7. Language Understanding & Ambiguity
- **Category**: Understanding
- **Description**: Assesses ability to resolve linguistic ambiguity and nuance
- **Scoring**: Disambiguation (10), nuance recognition (5), explanation clarity (5)
- **Max Score**: 20 points

### 8. Factual Knowledge & Retrieval
- **Category**: Knowledge
- **Description**: Tests accurate recall of factual information
- **Scoring**: Accuracy (10), completeness (5), specificity (3), reliability (2)
- **Max Score**: 20 points

### 9. Mathematical Problem Solving
- **Category**: Mathematics
- **Description**: Evaluates mathematical reasoning and computation
- **Scoring**: Correctness (10), methodology (5), step clarity (3), explanation (2)
- **Max Score**: 20 points

### 10. Ethical Reasoning & Nuance
- **Category**: Ethics
- **Description**: Tests ability to analyze complex ethical dilemmas
- **Scoring**: Framework understanding (5), balanced analysis (5), nuanced reasoning (5), thoughtfulness (5)
- **Max Score**: 20 points

Each task includes:
- Detailed evaluation input with specific requirements
- Expected output characteristics
- 2-3 development examples for few-shot prompting
- Structured evaluation criteria
- Weighted scoring rubric

## Prompting Strategies

The framework implements three distinct prompting strategies:

### Zero-Shot Prompting
- **Description**: Provides only the task description without examples
- **Use Case**: Baseline performance measurement
- **Format**: Task description + evaluation input
- **Supported Models**: All models

### Few-Shot Prompting
- **Description**: Includes 2-3 example solutions before the actual task
- **Use Case**: Demonstrates expected format and reasoning style
- **Format**: Examples section + task description + evaluation input
- **Supported Models**: All models

### Chain-of-Thought (CoT) Prompting
- **Description**: Explicitly requests step-by-step reasoning
- **Use Case**: Complex reasoning tasks requiring intermediate steps
- **Format**: Task with "think step-by-step" instructions
- **Supported Models**: Standard models only (not reasoning-specialized models)

**Important**: Reasoning-specialized models (e.g., DeepSeek-R1) do not use CoT prompting as they inherently employ step-by-step reasoning internally.

## Scripts Documentation

### run_evaluation.py

Main evaluation orchestrator that executes the complete evaluation pipeline.

**Usage**:
```bash
python scripts/run_evaluation.py [OPTIONS]
```

**Options**:
- `--tasks <task_ids>`: Comma-separated list of tasks to evaluate
- `--models <model_keys>`: Comma-separated list of models to use
- `--ollama-url <url>`: Ollama API endpoint (default: http://localhost:11434)
- `--results-dir <path>`: Results directory (default: data/results)
- `--verbose, -v`: Enable verbose logging
- `--skip-validation`: Skip Ollama connection validation
- `--list-tasks`: Display all available tasks and exit
- `--list-models`: Display all configured models and exit
- `--validate-tasks`: Show task completion status and exit

**Examples**:
```bash
# Run all evaluations
python scripts/run_evaluation.py

# Run specific tasks with verbose output
python scripts/run_evaluation.py --tasks code_generation,math_solving -v

# Run only small model
python scripts/run_evaluation.py --models small

# Check task status
python scripts/run_evaluation.py --validate-tasks
```

### generate_report.py

Generates CSV reports from scored JSON results with automatic total score calculation.

**Usage**:
```bash
python scripts/generate_report.py [RUN_ID] [OPTIONS]
```

**Arguments**:
- `RUN_ID`: Run identifier (e.g., run_2026-01-11_15-30-45)

**Options**:
- `--latest`: Use the most recent run
- `--results-dir <path>`: Results directory (default: data/results)
- `--verbose, -v`: Enable verbose logging

**Examples**:
```bash
# Process latest run
python scripts/generate_report.py --latest

# Process specific run
python scripts/generate_report.py run_2026-01-11_15-30-45

# Process with verbose output
python scripts/generate_report.py --latest -v
```

**Output**:
- Updates JSON files with calculated `total_score`
- Creates CSV file: `data/results/reports/<run_id>_results.csv`

### generate_plots.py

Creates comprehensive visualization plots from CSV reports.

**Usage**:
```bash
python scripts/generate_plots.py [CSV_PATH] [OPTIONS]
```

**Arguments**:
- `CSV_PATH`: Path to CSV file

**Options**:
- `--latest`: Use the most recent CSV report
- `--output-dir <path>`: Directory for saving plots
- `--format <format>`: Output format (png, pdf, svg; default: png)

**Examples**:
```bash
# Generate plots from latest report
python scripts/generate_plots.py --latest

# Generate PDF plots
python scripts/generate_plots.py --latest --format pdf

# Specify CSV and output directory
python scripts/generate_plots.py data/results/reports/run_xxx_results.csv --output-dir ./plots
```

**Output**: Creates `<run_id>_results_plots/` directory with 10 visualization files

## Directory Structure

```
LAB5/
├── src/llm_eval/           # Main source code
│   ├── tasks/             # Task definitions
│   │   ├── base.py       # Core data structures
│   │   ├── registry.py   # Task registry
│   │   └── definitions/  # Task implementations
│   ├── prompts/          # Prompting strategies
│   ├── models/           # Model configurations
│   ├── evaluation/       # Evaluation pipeline
│   └── results/          # Results management
├── scripts/              # Executable scripts
│   ├── run_evaluation.py    # Main evaluation runner
│   ├── generate_report.py   # CSV report generator
│   └── generate_plots.py    # Visualization generator
├── data/                 # Data directory
│   └── results/         # Evaluation results
│       ├── raw/         # JSON results by run
│       └── reports/     # CSV reports and plots
├── pyproject.toml       # Project dependencies
├── README.md           # This file
└── CLAUDE.md          # Development documentation
```

## Configuration

### Model Configuration

Models are defined in `src/llm_eval/models/config.py`:

```python
MODELS = {
    "small": ModelConfig(
        name="qwen2.5:1.5b",
        display_name="Qwen 2.5 (1.5B)",
        size_category="small",
        is_reasoning_model=False,
        parameters="1.5B",
        supported_strategies=["zero_shot", "few_shot", "chain_of_thought"],
        temperature=0.7,
        max_tokens=4096
    ),
    "large": ModelConfig(
        name="deepseek-r1:7b",
        display_name="DeepSeek R1 (7B)",
        size_category="large",
        is_reasoning_model=True,
        parameters="7B",
        supported_strategies=["zero_shot", "few_shot"],
        temperature=0.7,
        max_tokens=-1  # Unlimited tokens
    )
}
```

**Key Parameters**:
- `name`: Ollama model identifier
- `supported_strategies`: Which prompting strategies to use
- `is_reasoning_model`: If true, skips CoT (inherent reasoning)
- `max_tokens`: Token limit (-1 for unlimited)
- `temperature`: Sampling temperature (0.0-1.0)

### Adding New Models

1. Pull the model via Ollama:
```bash
ollama pull model-name:tag
```

2. Add configuration to `MODELS` dictionary in `config.py`
3. Specify appropriate `supported_strategies` based on model type
4. Run evaluation with new model:
```bash
python scripts/run_evaluation.py --models new_model_key
```

## Results and Analysis

### Result File Structure

Each evaluation produces a JSON file with the following structure:

```json
{
  "task_id": "logical_reasoning",
  "model_name": "qwen2.5:1.5b",
  "strategy": "few_shot",
  "prompt": "...",
  "response": "...",
  "timestamp": "2026-01-11T15:30:45.123456",
  "model_config": {...},
  "generation_time_ms": 3421,
  "prompt_tokens": 245,
  "completion_tokens": 187,
  "scores": {
    "logical_validity": 8,
    "completeness": 4,
    "clarity": 5
  },
  "total_score": 17,
  "evaluator_notes": "Strong logical reasoning with minor clarity issues"
}
```

### CSV Report Format

Generated CSV files include all fields from JSON, with columns:
- Identifiers: task_id, model_name, strategy
- Performance: scores (dict), total_score, evaluator_notes
- Metadata: timestamp, generation_time_ms, prompt_tokens, completion_tokens
- Config: model_config (JSON string)

### Interpreting Visualizations

**Plot 1-3**: Overall performance metrics
- Identify best-performing models
- Compare strategy effectiveness
- Assess consistency across tasks

**Plot 4-7**: Detailed analysis
- Heatmap shows task-specific strengths
- Distribution reveals consistency
- Time analysis informs deployment decisions
- Criteria breakdown identifies specific weaknesses

**Plot 8-10**: Task-model fit analysis
- Radar chart provides holistic view
- Winners plot shows task-specific leaders
- Specialization heatmap reveals relative strengths

## Extending the Framework

### Adding a New Task

1. Create task definition file in `src/llm_eval/tasks/definitions/`:

```python
from ..base import Task, TaskExample

def create_new_task() -> Task:
    return Task(
        id="new_task",
        name="New Task Name",
        category="Category",
        description="Task description",
        evaluation_input="Detailed evaluation prompt",
        expected_output_characteristics="What a good response looks like",
        development_examples=[
            TaskExample(
                input="Example input",
                output="Example output",
                explanation="Why this is a good example"
            )
        ],
        evaluation_criteria={
            "criterion1": "Description",
            "criterion2": "Description"
        },
        scoring_rubric={
            "criterion1": 10,
            "criterion2": 10
        },
        is_complete=True
    )
```

2. Register in `src/llm_eval/tasks/registry.py`:

```python
from .definitions.new_task import create_new_task

# Add to task_creators list in _load_tasks()
```

3. Test the new task:

```bash
python scripts/run_evaluation.py --tasks new_task --validate-tasks
```

### Adding a New Prompting Strategy

1. Create strategy class in `src/llm_eval/prompts/strategies.py`:

```python
class NewStrategy(PromptStrategy):
    def build_prompt(self, task: Task, **kwargs) -> str:
        # Implement prompt building logic
        pass
```

2. Register in `get_strategy()` function
3. Add to model's `supported_strategies` in config.py

## Requirements

### Core Dependencies

- Python >= 3.12
- requests >= 2.31.0
- rich >= 13.7.0
- pandas >= 2.1.0
- matplotlib >= 3.10.8
- seaborn >= 0.13.0

### External Dependencies

- Ollama (local installation)
- Compatible LLM models via Ollama

### Development Dependencies (Optional)

- pytest >= 7.4.0
- pytest-cov >= 4.1.0
- black >= 23.0.0
- ruff >= 0.1.0

## Troubleshooting

### Ollama Connection Issues

**Problem**: "Could not connect to Ollama"

**Solutions**:
1. Verify Ollama is running: `ollama list`
2. Check service status: `ps aux | grep ollama`
3. Restart Ollama: `ollama serve`
4. Verify URL: Default is `http://localhost:11434`

### Token Limit Exceeded

**Problem**: Responses are truncated or empty

**Solutions**:
1. Increase `max_tokens` in model config
2. Use `-1` for unlimited tokens (reasoning models)
3. Check model capabilities: Some models have hard limits

### Empty Scores in CSV

**Problem**: CSV shows null/empty scores

**Solutions**:
1. Ensure you completed Step 2 (manual scoring)
2. Verify `scores` field is properly formatted JSON
3. Run `generate_report.py` after adding scores

### Plot Generation Errors

**Problem**: Plots fail to generate

**Solutions**:
1. Ensure CSV has scored results: `scores` must not be null
2. For radar chart: Need at least 3 tasks
3. Check matplotlib backend: `export MPLBACKEND=Agg`
4. Install seaborn: `uv add seaborn`

### Task Not Found

**Problem**: "Task not found" error

**Solutions**:
1. List available tasks: `python scripts/run_evaluation.py --list-tasks`
2. Check task is marked complete: `--validate-tasks`
3. Verify task ID matches definition file

