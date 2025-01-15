

class Stream:
    """A streaming container to hold tokens.
    When adding tokens, the tokens are formatted (__format__) and appended to the container.
    """

    __input_format_hook__ = lambda self, x: format(x)
    __output_separator__ = " "

    def __init__(self, *args):
        self.tokens = []
        self(*args)

    def __call__(self, *args) -> "Stream":
        for a in args:
            self.tokens.append(self.__input_format_hook__(a))
        return self

    def __str__(self):
        return self.__output_separator__.join(self.tokens)


class text(Stream):
    """tokens in text are enclosed by double quotes."""

    __input_format_hook__ = lambda self, x: f"\"{x}\""



