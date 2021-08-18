from collections import defaultdict

from . import rsvp

COMMANDS = {
    "rsvp": rsvp
}
ALLOWED = ", ".join(list(map(lambda x: "`{0}`".format(x), COMMANDS.keys())))

DEFAULT_MESSAGE = """\n`{command}` is not a valid command. Please try one of the following:\n\n{commands}\n\n Or use `/help`""".format(command="{command}", commands=ALLOWED)

class Help(object):
    @classmethod
    def handle_action(cls, action, args, message):
        if not action:
            return "\nAvailable commands are:\n{commands}\n\nYou can also try:\n`/help [command]`".format(commands=ALLOWED)
        if action in COMMANDS:
            return COMMANDS[action].handle_help()
        else:
            DEFAULT_MESSAGE.format(command=command)

COMMANDS["help"] = Help()

def handle_command(command, action, args, message):
    if command not in COMMANDS:
        return DEFAULT_MESSAGE.format(command=command)
    return COMMANDS[command].handle_action(action, args, message)
