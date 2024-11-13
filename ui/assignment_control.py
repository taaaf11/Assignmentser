from __future__ import annotations

import typing

import flet as ft
import humanize

from utils import calculate_completed_tasks_quotient, calculate_completed_tasks_quotient_line

if typing.TYPE_CHECKING:
    from model import Assignment


class AssignmentControl(ft.Container):
    def __init__(self, assignment: Assignment, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.ProgressRing(
                            value=calculate_completed_tasks_quotient(assignment),
                            width=20,
                            height=20,
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.GREY,
                            tooltip=ft.Tooltip(calculate_completed_tasks_quotient_line(assignment)),
                        ),
                        ft.Text(
                            humanize.precisedelta(
                                assignment.deadline,
                                suppress=["minutes", "seconds"],
                                format="%0.0f",
                            ) + " left",
                        ),
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
