from __future__ import annotations
from typing import List
from AppCommandType import AppCommandType

class AppCommandDataOption(object):
    name: str
    type: AppCommandType
    value: str or int or float or bool
    options: List[AppCommandDataOption]
    focused: bool