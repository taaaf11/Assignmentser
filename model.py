from dataclasses import dataclass, field, asdict
from datetime import datetime

from enum import StrEnum, auto


class TaskStatus(StrEnum):
    PENDING = auto()
    COMPLETED = auto()


@dataclass
class Task:
    description: str
    status: TaskStatus = TaskStatus.PENDING

    @classmethod
    def from_dict(cls, task_data: dict):
        task_status = TaskStatus(task_data.pop('status'))
        return cls(
            **task_data,
            status=task_status,
        )


@dataclass
class Assignment:
    title: str
    description: str
    deadline: datetime
    tasks: list[Task] = field(default_factory=list)

    def __post_init__(self):
        if len(self.tasks) > 1 and self.tasks[0] == self.description:
            self.tasks.pop(0)

        if not self.tasks:
            self.tasks.append(Task(self.description))

    @classmethod
    def from_dict(cls, assignment_data: dict):
        deadline: datetime = datetime.fromisoformat(assignment_data.pop('deadline'))
        tasks = [Task.from_dict(task_data) for task_data in assignment_data.pop('tasks')]

        return cls(
            **assignment_data,
            tasks=tasks,
            deadline=deadline,
        )

    def as_dict(self):
        deadline = self.deadline.isoformat()
        self_dict = asdict(self)
        self_dict.update({'deadline': deadline})
        return self_dict
