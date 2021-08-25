from ..schema import get_session
from ..schema.roles import Role
from ..utils.error import BlebotError

def check_role(command, message):
    server, channel = message.server, message.channel

    # Check if the role exists
    session = get_session(message.server.id)

    role = session.query(Role).filter(
        Role.channel == channel.id
    ).first()

    if not role or not role.modules or command not in role.modules:
        raise BlebotError("The command:`{module}` is not enabled for this channel! \nPlease assign it by using `/enable #{channel} {module}`".format(
            channel=message.channel,
            module=command
        ))
    return role
