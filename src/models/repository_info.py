from dataclasses import dataclass


@dataclass
class RepositoryInfo:
    path: str
    branches: list[str]