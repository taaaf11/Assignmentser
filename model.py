from dataclasses import dataclass


@dataclass
class Assignment:
    title: str
    description: str


@dataclass
class Task:
    description: str
