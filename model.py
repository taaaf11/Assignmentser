from dataclasses import dataclass, field


@dataclass
class Assignment:
    title: str
    description: str
    tasks: list[str] = field(default_factory=list)
