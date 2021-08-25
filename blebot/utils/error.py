class BlebotError(Exception):
    def __init__(self, message):
        super(Exception,self).__init__(
            "\nOh no! I've encountered some troubles\n\t{message}".format(
                message="\n\t".join(message.split("\n"))
            )
        )
