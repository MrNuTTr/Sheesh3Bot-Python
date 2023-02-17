from typing import List
from InteractionType import InteractionType
from AppCommandDataOption import AppCommandDataOption

"""Sent in APPLICATION_COMMAND and 
APPLICATION_COMMAND_AUTOCOMPLETE interactions."""
class InteractionData:
    id: int
    name: str
    type: InteractionType
    resolved: ResolvedData
    options: List[AppCommandDataOption]
    guild_id: int
    target_id: int