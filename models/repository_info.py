from dataclasses import dataclass


@dataclass
class RepositoryInfo:
    path: str
    local_branches: list[str]
    remote_branches: list[str]