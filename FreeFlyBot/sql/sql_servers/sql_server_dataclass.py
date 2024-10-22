from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ServerData:
    id: int
