from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:
    event_id: int
    server_id: int
    event_name: str
    type_id: int
    comment: str
    event_time: datetime


@dataclass
class Type:
    type_id: int
    server_id: int
    type_name: str
    channel: str
    
@dataclass    
class DiscordServer:
    server_id: int
    server_name: str
    
@dataclass   
class Pilot:
    pilot_id: int
    name: str
    discord_nick: str
    
@dataclass    
class PilotRole:
    pilot_id: int
    type_id: int
    
    

