from datetime import datetime

import flet as ft

from model import Assignment
from storage import Storage


class AssignmentCreateControl(ft.Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.content = ft.Column(
            [
                # title
                ft.Text("Title:"),
                title_textfield := ft.TextField(multiline=True, width=300),
                # description
                ft.Text("Description:"),
                description_textfield := ft.TextField(multiline=True, width=300),
                # deadline
                ft.Text("Deadline:"),
                deadline_textfield := ft.TextField(read_only=True, width=300),
                ft.IconButton(
                    ft.icons.DATE_RANGE,
                    on_click=lambda _: self.page.open(
                        ft.DatePicker(on_change=self.set_deadline_date)
                    ),
                ),
            ],
            tight=True,
        )

        self.title_textfield = title_textfield
        self.description_textfield = description_textfield
        self.deadline_textfield = deadline_textfield
        self.deadline_value: datetime | None = None

        self.width = 350

    def set_deadline_date(self, e):
        self.deadline_textfield.value = e.control.value.isoformat()
        self.deadline_value = e.control.value
        self.deadline_textfield.update()

    def validate(self):
        return (
            len(self.title_textfield.value)
            and len(self.description_textfield.value)
            and len(self.deadline_textfield.value)
        )

    async def get_assignment(self) -> Assignment:
        if not self.validate():
            return

        assignment = Assignment(
            id=await Storage.get_new_assignment_id(),
            title=self.title_textfield.value,
            description=self.description_textfield.value,
            deadline=self.deadline_value,
        )
        await Storage.store_assignment(assignment)
        return assignment
