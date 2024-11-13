import flet as ft

from model import Assignment
from storage import Storage
from ui.assignment_control import AssignmentControl


class AssignmentsListControl(ft.Column):
    def __init__(self, assignments: list[Assignment], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.controls = self._prepare_assignment_controls(assignments)

    @staticmethod
    def _prepare_assignment_controls(assignments: list[Assignment]):
        return [AssignmentControl(assignment) for assignment in assignments]

    def add(self, assignment_control: AssignmentControl):
        self.controls.append(assignment_control)
        self.update()

    async def reload(self):
        self.controls = self._prepare_assignment_controls(await Storage.retrieve_assignments())
        self.update()
