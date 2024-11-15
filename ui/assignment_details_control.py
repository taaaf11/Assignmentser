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
            # value=calculate_completed_tasks_quotient(
            #     assignment
            # ),
            value=completed_tasks_quotient,
            # value=1/6,
            width=160,
            color=ft.colors.WHITE,
            bgcolor=ft.colors.GREY,
        )

        self.tasks_column = ft.Column(
            TaskControl(assignment, task, self.update_progress_bar)
            for task in assignment.tasks
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
                                ft.Text(
                                    f"{(completed_tasks_quotient * 100):.0f}% done"
                                ),
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

    async def add_task_control(self, _):
        self.tasks_column.controls.append(TaskControl(self.assignment))
        self.update()

    def _show_task_create_dialog(self, _):
        async def _save_task(_):
            self.assignment.tasks.append(Task(task_textfield.value))
            await Storage.store_assignments([self.assignment])

        self.page.open(
            ft.AlertDialog(
                content=ft.Row(
                    [
                        ft.Text("Task:"),
                        task_textfield := ft.TextField(),
                    ],
                    tight=True,
                ),
                actions=[ft.IconButton(ft.icons.CHECK, on_click=_save_task)],
            )
        )

    def update_progress_bar(self):
        completed_tasks_quotient = (
            0
            if len(self.assignment.tasks) == 0
            else calculate_completed_tasks_quotient(self.assignment)
        )
        self.completed_tasks_quotient_progress_bar.value = completed_tasks_quotient
        self.completed_tasks_quotient_progress_bar.update()

    def _build_tasks_controls(self) -> list[ft.Control]:
        tasks = self.assignment.tasks
        if len(tasks) > 1:
            return [
                ft.Text("Tasks:", font_family="Open-Sans", weight=ft.FontWeight.W_400),
                *[TaskControl(self.assignment, task) for task in tasks],
            ]
        else:
            return [ft.Container()]
