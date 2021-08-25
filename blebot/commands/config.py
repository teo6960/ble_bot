COMMANDS = {}
ALLOWED = lambda: ", ".join(list(map(lambda x: "`{0}`".format(x), list(COMMANDS.keys()))))
DEFAULT_MESSAGE = """\n`{command}` is not a valid command. Please try one of the following:\n\n{commands}\n\n Or use `/help`"""
