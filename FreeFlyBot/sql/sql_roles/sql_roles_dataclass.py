from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RoleData:
    id: int
    server_id: int
    name: str
