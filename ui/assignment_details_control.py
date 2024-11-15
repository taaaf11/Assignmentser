import flet as ft

from model import Assignment, Task
from storage import Storage
from ui.task_control import TaskControl
from utils import calculate_completed_tasks_quotient


class AssignmentDetailsControl(ft.Container):
    def __init__(self, assignment: Assignment, page: ft.Page, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assignment = assignment

        completed_tasks_quotient = (
            0
            if len(assignment.tasks) == 0
            else calculate_completed_tasks_quotient(assignment)
        )
        self.completed_tasks_quotient_progress_bar = ft.ProgressBar(
            value=completed_tasks_quotient,
            width=160,
            color=ft.colors.WHITE,
            bgcolor=ft.colors.GREY,
        )
        self.completed_tasks_quotient_percentage_text = ft.Text(
            f"{(completed_tasks_quotient * 100):.0f}% done"
        )

        self.tasks_column = ft.Column(
            [
                TaskControl(
                    assignment,
                    task,
                    self.update_display_values,
                    on_delete=lambda task: self.delete_task(task),
                )
                for task in assignment.tasks
            ],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True,
        )
        self.content = ft.Stack(
            [
                ft.Column(
                    [
                        ft.Text(
                            assignment.title,
                            font_family="Open-Sans",
                            size=25,
                            weight=ft.FontWeight.W_900,
                        ),
                        ft.Text(
                            assignment.description,
                            font_family="Open-Sans",
                            size=19,
                            weight=ft.FontWeight.W_500,
                        ),
                        ft.Container(height=20),
                        ft.Column(
                            [
                                ft.Container(
                                    self.completed_tasks_quotient_progress_bar,
                                    alignment=ft.alignment.center,
                                ),
                                self.completed_tasks_quotient_percentage_text,
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Container(height=20),
                        self.tasks_column,
                        # *self._build_tasks_controls(),
                    ],
                    tight=True,
                ),
                ft.FloatingActionButton(
                    ft.icons.ADD,
                    bottom=8,
                    right=20,
                    on_click=self.add_task_control,
                ),
            ],
        )

        self.width = page.window.width - 400
        # self.height = page.height - 200

    def delete_task(self, task: Task):
        task_control: TaskControl
        for task_control in self.tasks_column.controls.copy():
            if task_control.task == task:
                self.tasks_column.controls.remove(task_control)
        self.assignment.tasks.remove(task)
        self.tasks_column.update()
        self.update_display_values()

    async def add_task_control(self, _):
        try:
            if self.tasks_column.controls[0].task.description == self.assignment.description:
                self.tasks_column.controls.pop(0)
                await Storage.delete_task_from_assignment(self.assignment.id, self.assignment.tasks.pop(0))
        except IndexError:
            pass
        self.tasks_column.controls.append(
            TaskControl(
                self.assignment,
                on_change=self.update_display_values,
                on_description_submit=self.update_display_values,
                on_delete=self.delete_task,
            )
        )
        self.update()

    def update_display_values(self):
        completed_tasks_quotient = (
            0
            if len(self.assignment.tasks) == 0
            else calculate_completed_tasks_quotient(self.assignment)
        )
        self.completed_tasks_quotient_percentage_text.value = (
            f"{completed_tasks_quotient * 100:.0f}% done"
        )
        self.completed_tasks_quotient_progress_bar.value = completed_tasks_quotient
        self.update()

    def _build_tasks_controls(self) -> list[ft.Control]:
        tasks = self.assignment.tasks
        if len(tasks) > 1:
            return [
                ft.Text("Tasks:", font_family="Open-Sans", weight=ft.FontWeight.W_400),
                *[TaskControl(self.assignment, task) for task in tasks],
            ]
        else:
            return [ft.Container()]
