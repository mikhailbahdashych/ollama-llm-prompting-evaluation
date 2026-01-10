"""Task registry for managing evaluation tasks."""

import logging
from typing import Dict, List, Optional

from .base import Task

# Import task creation functions
from .definitions.instruction_following import create_instruction_following_task
from .definitions.logical_reasoning import create_logical_reasoning_task
from .definitions.creative_writing import create_creative_writing_task
from .definitions.code_generation import create_code_generation_task
from .definitions.reading_comprehension import create_reading_comprehension_task
from .definitions.common_sense import create_common_sense_task
from .definitions.language_understanding import create_language_understanding_task
from .definitions.factual_knowledge import create_factual_knowledge_task
from .definitions.math_solving import create_math_solving_task
from .definitions.ethical_reasoning import create_ethical_reasoning_task


logger = logging.getLogger(__name__)


class TaskRegistry:
    """Registry for managing and accessing evaluation tasks.

    The registry loads all task definitions and provides methods to
    retrieve tasks by ID or category.
    """

    def __init__(self):
        """Initialize the task registry and load all tasks."""
        self._tasks: Dict[str, Task] = {}
        self._load_tasks()

    def _load_tasks(self):
        """Load all task definitions."""
        task_creators = [
            create_instruction_following_task,
            create_logical_reasoning_task,
            create_creative_writing_task,
            create_code_generation_task,
            create_reading_comprehension_task,
            create_common_sense_task,
            create_language_understanding_task,
            create_factual_knowledge_task,
            create_math_solving_task,
            create_ethical_reasoning_task
        ]

        for creator in task_creators:
            try:
                task = creator()
                self._tasks[task.id] = task
                logger.debug(f"Loaded task: {task.id}")
            except Exception as e:
                logger.error(f"Failed to load task from {creator.__name__}: {e}")

        logger.info(f"Loaded {len(self._tasks)} tasks")

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by its ID.

        Args:
            task_id: The task identifier

        Returns:
            Task object if found, None otherwise
        """
        task = self._tasks.get(task_id)
        if task is None:
            logger.warning(f"Task not found: {task_id}")
        return task

    def get_all_tasks(self) -> List[Task]:
        """Get all registered tasks.

        Returns:
            List of all Task objects
        """
        return list(self._tasks.values())

    def get_tasks_by_category(self, category: str) -> List[Task]:
        """Get all tasks in a specific category.

        Args:
            category: The category name

        Returns:
            List of Task objects in the category
        """
        return [task for task in self._tasks.values() if task.category == category]

    def get_task_ids(self) -> List[str]:
        """Get all task IDs.

        Returns:
            List of task identifiers
        """
        return list(self._tasks.keys())

    def count_complete_tasks(self) -> int:
        """Count tasks that are complete (no TODO markers).

        Returns:
            Number of complete tasks
        """
        return sum(1 for task in self._tasks.values() if task.is_complete())

    def count_incomplete_tasks(self) -> int:
        """Count tasks that still have TODO markers.

        Returns:
            Number of incomplete tasks
        """
        return sum(1 for task in self._tasks.values() if not task.is_complete())

    def get_completion_status(self) -> Dict[str, bool]:
        """Get completion status for all tasks.

        Returns:
            Dict mapping task_id to completion status (True if complete)
        """
        return {task_id: task.is_complete() for task_id, task in self._tasks.items()}

    def validate_tasks(self) -> Dict[str, List[str]]:
        """Validate all tasks and report incomplete fields.

        Returns:
            Dict mapping task_id to list of incomplete field names
        """
        validation_report = {}
        for task_id, task in self._tasks.items():
            incomplete_fields = task.get_incomplete_fields()
            if incomplete_fields:
                validation_report[task_id] = incomplete_fields
        return validation_report
