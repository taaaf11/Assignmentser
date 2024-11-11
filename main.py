import flet as ft

from model import Assignment
from ui.assignment_control import AssignmentControl


def main(page: ft.Page):
    page.add(AssignmentControl(Assignment('hello world', 'hello world description')))
    ...


ft.app(main)