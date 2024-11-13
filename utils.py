from __future__ import annotations

import typing

from model import TaskStatus

if typing.TYPE_CHECKING:
    from model import Assignment


def calculate_completed_tasks_quotient(assignment: Assignment) -> float:
    """
    Return: "{completed tasks} / {all_tasks}"
    Example: "1 / 6"
    """

    completed_len = len([task for task in assignment.tasks if task.status == TaskStatus.COMPLETED])
    all_len = len(assignment.tasks)

    return completed_len / all_len


def calculate_completed_tasks_quotient_line(assignment: Assignment) -> str:
    """
    Return: "{completed tasks} / {all_tasks} tasks done"
    Example: "1 / 6 tasks done"
    """

    completed_len = len([task for task in assignment.tasks if task.status == TaskStatus.COMPLETED])
    all_len = len(assignment.tasks)

    return f"{completed_len} / {all_len} tasks done"
