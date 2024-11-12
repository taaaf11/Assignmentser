from dataclasses import dataclass, field
from datetime import datetime as dt_class


@dataclass
class Assignment:
    title: str
    description: str
    deadline: dt_class
    tasks: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, assignment_data: dict):
        deadline: dt_class = dt_class.fromisoformat(assignment_data.pop('deadline'))
        return cls(
            **assignment_data,
            deadline=deadline,
        )
