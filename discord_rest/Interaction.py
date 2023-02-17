from InteractionType import InteractionType
from InteractionData import InteractionData

"""_summary_
    An Interaction is the message that your application receives when a user 
    uses an application command or a message component.
    
    For Slash Commands, it includes the values that the user submitted.
    
    For User Commands and Message Commands, it includes the resolved user or 
    message on which the action was taken.

    For Message Components it includes identifying information about the 
    component that was used. It will also include some metadata about how the 
    interaction was triggered: the guild_id, channel_id, member and other 
    fields. You can find all the values in our data models below.
    
    https://discord.com/developers/docs/interactions/receiving-and-responding#interactions
"""
class Interaction:
    """ID of the interaction
    """; id: int
    """ID of the application this interaction is for
    """; application_id: int
    """Type of interaction
    """; type: InteractionType
    """Interaction data payload
    """; data: InteractionData
    """Guild taht the interaction was sent from
    """; guild_id: int
    """Channel that the interaction was sent from
    """; channel_id: int
    """Guild member data for the invoking using, including permissions
    """; member: guildMember
    """User object for the invoking user, if invoked in a DM
    """; user: User
    """Continuation token for responding to the interaction
    """; token: str
    """Read-only property, always 1
    """; version: int
    """For components, the message they were attached to
    """; message: Message
    """Bitwise set of permissions the app or bot has within the channel the
    interaction was from.
    """; app_permissions: str
    """Selected language of the invoking user
    """; locale: str
    """Guild's preferred locale, if invoked in a guild
    """; guild_locale: str
    
    def __init__(self):
        return
    
    