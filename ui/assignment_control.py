from __future__ import annotations

import typing

import flet as ft

if typing.TYPE_CHECKING:
    from model import Assignment


class AssignmentControl(ft.Container):
    def __init__(self, assignment: Assignment, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.content = ft.Column(
            controls=[
                ft.Text(assignment.title, weight=ft.FontWeight.BOLD),
                ft.Text(assignment.description, weight=ft.FontWeight.W_300)
            ]
        )
