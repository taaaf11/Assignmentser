from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING

from model import Assignment

if TYPE_CHECKING:
    from flet_core.client_storage import ClientStorage


class Storage:
    """
    A convenience class providing functions for easy
    storage and retrieval of data
    """
    _instance: ClientStorage | None = None
    _assignments_prefix = 'taaaf11-Assignmentser-assignments-data'

    @staticmethod
    def init(client_storage: ClientStorage):
        Storage._instance = client_storage

    @staticmethod
    async def _get(key: str) -> Any:
        return await Storage._instance.get_async(key)

    @staticmethod
    async def _set(key: str, value: Any) -> None:
        await Storage._instance.set_async(key, value)

    @staticmethod
    async def retrieve_assignments() -> list[Assignment]:
        assignments_data: Optional[list[dict]] = await Storage._get(Storage._assignments_prefix)
        if assignments_data is not None:
            return [Assignment.from_dict(assignment_data) for assignment_data in assignments_data]
        return []

    @staticmethod
    async def store_assignment(assignment: Assignment) -> None:
        stored = (await Storage.retrieve_assignments()) or []
        stored = [assignment.as_dict() for assignment in stored]
        stored.append(assignment.as_dict())
        await Storage._set(Storage._assignments_prefix, stored)

    @staticmethod
    async def clear_data() -> None:
        await Storage._instance.remove_async(Storage._assignments_prefix)
