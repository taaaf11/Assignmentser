from __future__ import annotations

import typing
import datetime as dt

import flet as ft
import humanize

from model import TaskStatus

if typing.TYPE_CHECKING:
    from model import Assignment


class AssignmentControl(ft.Container):
    def __init__(self, assignment: Assignment, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def calculate_completed_tasks_quotient() -> float:
            completed_len = len([task for task in assignment.tasks if task.status == TaskStatus.COMPLETED])
            all_len = len(assignment.tasks)


            return completed_len / all_len


        def calculate_completed_tasks_quotient_line() -> str:
            completed_len = len([task for task in assignment.tasks if task.status == TaskStatus.COMPLETED])
            all_len = len(assignment.tasks)

            return f"{completed_len} / {all_len} tasks done"

        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.ProgressRing(
                            value=calculate_completed_tasks_quotient(),
                            width=20,
                            height=20,
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.GREY,
                            tooltip=ft.Tooltip(calculate_completed_tasks_quotient_line()),
                        ),
                        ft.Text(humanize.precisedelta(assignment.deadline, suppress=["minutes", "seconds"], format="%0.0f")),
                        ft.Icon(ft.icons.MORE_VERT, color=ft.colors.WHITE),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Text(assignment.title, weight=ft.FontWeight.BOLD),
                ft.Text(assignment.description, weight=ft.FontWeight.W_300)
            ]
        )

        # borders
        self.border = ft.border.all(3, ft.colors.WHITE)
        self.border_radius = ft.border_radius.all(10)

        # margins
        self.padding = ft.padding.all(18)
