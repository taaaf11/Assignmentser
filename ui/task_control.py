from collections.abc import Callable

import flet as ft

from model import Assignment, Task, TaskStatus
from storage import Storage


class TaskControl(ft.Row):
    def __init__(
        self,
        assignment: Assignment,
        task: Task | None = None,
        on_change: Callable | None = None,
        on_description_submit: Callable | None = None,
        on_delete: Callable | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.assignment = assignment
        self.task = task
        self.on_change = on_change
        self.on_description_submit = on_description_submit
        self.on_delete = on_delete

        if task is not None:
            self.check_icon = ft.IconButton(
                ft.icons.CHECK_BOX
                if task.status == TaskStatus.COMPLETED
                else ft.icons.CHECK_BOX_OUTLINE_BLANK,
                on_click=self.update_status,
            )
            self.description_textfield = ft.TextField(
                visible=False, on_submit=self._show_description_text
            )
            self.description_text_control = ft.Text(task.description)
        else:
            self.check_icon = ft.IconButton(
                ft.icons.CHECK_BOX_OUTLINE_BLANK,
                on_click=self.update_status,
            )
            self.description_textfield = ft.TextField(
                on_submit=self._show_description_text
            )
            self.description_text_control = ft.Text(visible=False)

        self.controls = [
            ft.Row([
            self.check_icon,
            self.description_textfield,
            self.description_text_control,
            ]),
            # ft.Container(width=self.len_longest_task_description()),
            ft.IconButton(ft.icons.DELETE_OUTLINE, on_click=self.delete)
        ]
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

    def len_longest_task_description(self):
        lengths = (len(task.description) for task in self.assignment.tasks)
        return max(lengths)

    async def _show_description_text(self, _):
        self.description_text_control.value = self.description_textfield.value
        self.description_text_control.visible = True
        self.description_textfield.visible = False
        self.task = Task(self.description_text_control.value)
        await self.add_task(_)
        self.update()

    async def add_task(self, _):
        await Storage.add_task_to_assignment(self.assignment.id, self.task)
        self.assignment.tasks.append(self.task)
        self.on_description_submit()
        await self.page.assignments_list.reload()

    async def delete(self, _):
        await Storage.delete_task_from_assignment(self.assignment.id, self.task)
        self.on_delete(self.task)

    async def update_status(self, _):
        new_status: TaskStatus
        match self.task.status:
            case TaskStatus.PENDING:
                new_status = TaskStatus.COMPLETED
                self.check_icon.icon = ft.icons.CHECK_BOX
            case TaskStatus.COMPLETED:
                new_status = TaskStatus.PENDING
                self.check_icon.icon = ft.icons.CHECK_BOX_OUTLINE_BLANK

        self.task.status = new_status
        self.check_icon.update()
        if self.on_change:
            self.on_change()

        await Storage.update_task_status(self.assignment.id, self.task, new_status)
        await self.page.assignments_list.reload()
