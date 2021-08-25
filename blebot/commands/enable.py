import re

from .config import COMMANDS
from ..schema import get_session
from ..schema.roles import Role
from ..utils.error import BlebotError

ACTION_PATTERN = re.compile(r"<#([0-9]*)>")

def handle_action(command, action, args, message, role=None):
    if args not in COMMANDS.keys() or args in ["help", "enable"]:
        raise BlebotError("`{module}` is not a module available to be enabled.\nExisting modules are:\n{existing}".format(
            module=args,
            existing=", ".join(list(map(lambda x: "`{0}`".format(x), [key for key in COMMANDS.keys() if key not in ["help", "enable"]])))
        ))

    # Validate Action
    action = ACTION_PATTERN.match(action)
    action = action.group(1) if action else None

    if not message.channel_mentions or message.channel_mentions[0].id != action:
        raise BlebotError("Please make sure you mention the channel using the `#`\n i.e. `/enable #raids rsvp`")

    # Grab Channel & Server information
    channel_id = message.channel_mentions[0].id
    server_id = message.server.id

    session = get_session(message.server.id)
    existing_role = session.query(Role).filter(Role.channel == channel_id).first()

    if not existing_role:
        existing_role = Role(server_id, channel_id, {
            "created_by_id": message.author.id,
            "created_by": message.author.name
        })

    if args in existing_role.modules:
        raise BlebotError("The module `{module}` already exists in that channel!".format(module = args))

    existing_role.modules.add(args)
    session.add(existing_role)
    session.commit()

    return "\nEnabled {module} for channel #{channel}".format(module=args, channel=message.channel_mentions[0].name)


def handle_help():
    return "\n`enable`: Enables a module for a particular channel.\n\ti.e. `/enable #[channel] [module]`"
