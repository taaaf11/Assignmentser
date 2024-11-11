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
    async def store_assignment(assignment: Assignment):
        await Storage._set(Storage._assignments_prefix, assignment)

    @staticmethod
    async def retrieve_assignments() -> list[Assignment]:
        assignments: Optional[Assignment] = await Storage._get(Storage._assignments_prefix)
        return assignments or []
