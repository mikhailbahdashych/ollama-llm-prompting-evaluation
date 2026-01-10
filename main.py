"""Main entry point for the LLM evaluation system.

This is a simple wrapper that runs the main evaluation script.
For more options, use: python scripts/run_evaluation.py --help
"""

import subprocess
import sys


def main():
    """Run the evaluation script."""
    print("Starting LLM Evaluation System")
    print("=" * 50)
    print()
    print("For available options, run: python scripts/run_evaluation.py --help")
    print()
    print("Quick commands:")
    print("  - List all tasks: python scripts/run_evaluation.py --list-tasks")
    print("  - List all models: python scripts/run_evaluation.py --list-models")
    print("  - Validate tasks: python scripts/run_evaluation.py --validate-tasks")
    print("  - Run evaluations: python scripts/run_evaluation.py")
    print()
    print("=" * 50)
    print()

    # Forward to the actual script
    subprocess.run([sys.executable, "scripts/run_evaluation.py"] + sys.argv[1:])


if __name__ == "__main__":
    main()
