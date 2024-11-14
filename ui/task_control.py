import flet as ft

from model import Assignment, Task, TaskStatus
from storage import Storage


class TaskControl(ft.Checkbox):
    def __init__(self, assignment: Assignment, task: Task, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.assignment = assignment
        self.task = task

        self.value = task.status == TaskStatus.COMPLETED
        self.label = task.description
        self.on_change = self.update_status

    async def update_status(self, _):
        new_state: TaskStatus
        match self.task.status:
            case TaskStatus.PENDING:
                new_state = TaskStatus.COMPLETED
            case TaskStatus.COMPLETED:
                new_state = TaskStatus.PENDING

        self.assignment.tasks[self.assignment.tasks.index(self.task)].status = new_state
        await self.page.assignments_list.save_assignments()
