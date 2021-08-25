from .config import DEFAULT_MESSAGE, COMMANDS, ALLOWED

def handle_action(command, action, args, message, role=None):
    if not action:
        return "\nAvailable commands are:\n{commands}\n\nYou can also try:\n`/help [command]`".format(commands=ALLOWED())
    if action in COMMANDS:
        return COMMANDS[action].handle_help()
    else:
        return DEFAULT_MESSAGE.format(command=action, commands=ALLOWED())
