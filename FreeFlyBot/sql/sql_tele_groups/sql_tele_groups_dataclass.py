from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GroupData:
    id: int
    server_id: int
    require_role_id: int
