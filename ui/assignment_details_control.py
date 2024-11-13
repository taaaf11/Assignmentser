import flet as ft

from model import Assignment
from utils import calculate_completed_tasks_quotient


class AssignmentDetailsControl(ft.Container):
    def __init__(self, assignment: Assignment, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.content = ft.Column(
            [
                ft.Text(assignment.title),
                ft.Text(assignment.description),
                # ft.ProgressBar(value=calculate_completed_tasks_quotient(assignment)),
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.ProgressBar(
                                    value=calculate_completed_tasks_quotient(assignment),
                                    # value=1/6,
                                    width=430,
                                    color=ft.colors.WHITE,
                                    bgcolor=ft.colors.GREY,
                                ),
                                ft.Text(
                                    f"{calculate_completed_tasks_quotient(assignment) * 100}% done"
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        )
                    ],
                    # width=50,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                *[
                    ft.Checkbox(task.description)
                    for task in assignment.tasks
                ]
            ]
        )
