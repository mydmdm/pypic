

class Annotatable:
    """A base class for objects that can be annotated.
    Types of annotations:
    - unary_annotations: behaves like a store_true action
        if called, append the annotation name to the tokens
        example: bold(), italic(), big(), small(), fit()
    - binary_annotations: behaves like a key-value pair
        if called with an argument, append the annotation name and the argument to the tokens
        example: ht("10"), wid("20"), rad("5"), color("red"), fill("blue")
    """

    unary_annotations = ()
    binary_annotations = ()

    def __init__(self):
        pass
        # add annotate method to text
        for a in self.unary_annotations:
            setattr(self, a, lambda x=a: self(x))

        # add annotate_with_value method to text
        for a in self.binary_annotations:
            setattr(self, a, lambda value, x=a: self(x)(value))
            # setattr(self, a, lambda value, x=a: self.annotate_with_value(x, value))

    # # annotation for type hinting
    # def annotate(self, annotation: str):
    #     self.tokens.append(format(annotation))
    #     return self

    # def annotate_with_value(self, annotation: str, value: str):
    #     self.tokens.extend([annotation, format(value)])
    #     return self

    def __call__(self, *args) -> "Annotatable":
        for a in args:
            self.tokens.append(format(a))
        return self


class text(Annotatable):

    unary_annotations = ("bold", "italic", "big", "small", "fit")

    def __init__(self, *contents: str):
        super().__init__()
        self.tokens = []
        for content in contents:
            # add double quotes to text_info and then append to info
            self.tokens.append(f"\"{content}\"")

    def __format__(self, format_spec: str):
        self.validate()
        return " ".join(self.tokens)

    def validate(self) -> bool:
        """Check if the text is valid."""
        # fit rule: only one fit is allowed, and it must be the last token
        if self.tokens.count("fit") > 1:
            raise ValueError("Only one fit is allowed.")
        if "fit" in self.tokens[:-1]:
            raise ValueError("fit must be the last annotation for a text.")
        return True

    # override the + operator
    def __add__(self, other):
        s = text(None)
        s.tokens = self.tokens + other.tokens
        return s


