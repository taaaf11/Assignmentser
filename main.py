import flet as ft

from storage import Storage
from ui.assignment_control import AssignmentControl
from ui.assignment_create_control import AssignmentCreateControl
from ui.assignment_details_control import AssignmentDetailsControl
from ui.assignments_list_column import AssignmentsListControl


async def main(page: ft.Page):
    Storage.init(page.client_storage)

    async def show_assignment_create_dialog(_):
        async def add_assignment_control_to_page(_):
            page.assignments_list.add(AssignmentControl(await crt_control.get_assignment()))
            page.close(dialog)

        crt_control = AssignmentCreateControl()
        dialog = ft.AlertDialog(
                content=crt_control,
                actions=[ft.IconButton(ft.icons.CHECK, on_click=add_assignment_control_to_page)]
        )
        page.open(dialog)


    page.scroll = ft.ScrollMode.AUTO

    page.fonts = {
        'Comfortaa': 'assets/fonts/Comfortaa-VariableFont_wght.ttf',
        'Open-Sans': 'assets/fonts/OpenSans-VariableFont_wdth,wght.ttf',
    }

    assignments = await Storage.retrieve_assignments()
    page.floating_action_button = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=show_assignment_create_dialog)
    page.assignments_list = AssignmentsListControl(assignments)
    page.add(page.assignments_list)


ft.app(main)