from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ResponseData:
    status: int
    json: dict
