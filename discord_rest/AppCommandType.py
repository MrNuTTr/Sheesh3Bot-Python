from enum import Enum

class AppCommandType(Enum):
    SUB_COMMAND = 1
    SUB_COMMAAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10
    ATTACHMENT = 11