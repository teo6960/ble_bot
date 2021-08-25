from .config import COMMANDS, ALLOWED, DEFAULT_MESSAGE
from ..utils.auth import check_role
from . import rsvp, help, enable
from ..utils.error import BlebotError

def handle_command(command, action, args, message):
    if action: action = action.strip()
    if command: command = command.strip()
    if args: args = args.strip()

    if command not in COMMANDS:
        return DEFAULT_MESSAGE.format(command=command, commands=ALLOWED())

    if command and not action:
        return COMMANDS["help"].handle_action("help", command, action, message)

    if command in ["enable", "help"]:
        return COMMANDS[command].handle_action(command, action, args, message)

    role = check_role(command, message)
    return COMMANDS[command].handle_action(command, action, args, message, role)

def initialize():
    COMMANDS.update(
        {
            "help": help,
            "enable": enable,
            "rsvp": rsvp
        }
    )
