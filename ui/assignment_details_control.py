import flet as ft

from model import Assignment
from utils import calculate_completed_tasks_quotient


class AssignmentDetailsControl(ft.Container):
    def __init__(self, assignment: Assignment, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.assignment = assignment
        self.content = ft.Column(
            [
                ft.Text(
                    assignment.title,
                    font_family='Open-Sans',
                    size=25,
                    weight=ft.FontWeight.W_900,
                ),
                ft.Text(
                    assignment.description,
                    font_family='Open-Sans',
                    size=19,
                    weight=ft.FontWeight.W_500,
                ),
                ft.Container(height=20),
                ft.Column(
                    [
                        ft.Container(
                            ft.ProgressBar(
                                value=calculate_completed_tasks_quotient(assignment),
                                # value=1/6,
                                width=160,
                                color=ft.colors.WHITE,
                                bgcolor=ft.colors.GREY,
                            ),
                            alignment=ft.alignment.center,
                        ),
                        ft.Text(
                            f"{calculate_completed_tasks_quotient(assignment) * 100}% done"
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Container(height=20),
                self._build_tasks_controls()
            ],
            # tight=True,
        )

    def _build_tasks_controls(self):
        tasks = self.assignment.tasks
        if len(tasks) > 1:
            return [
                ft.Text('Tasks:', font_family='Open-Sans', weight=ft.FontWeight.W_400),
                *[
                    ft.Checkbox(task.description)
                    for task in tasks
                ],
            ]
        else:
            return ft.Container()
