##################################
# Pikchr Objects
# https://pikchr.org/home/doc/trunk/doc/grammar.md
##################################
from .utils import text, Annotatable

ctrl_objects: list[str] = ['var', 'statement']
line_objects: list[str] = ["arrow", "arc", "line", "move", "spline"]
shape_objects: list[str] = [
    "box",
    "circle",
    "cylinder",
    "diamond",
    "ellipse",
    "file",
    "oval",
]


class PikchrObject(Annotatable):

    def __init__(self, object_type: str, label: str = None, *attributes: str):
        super().__init__()
        self.object_type = object_type
        self.label = label
        self.tokens: list[str] = []

        if label is not None and self.object_type in shape_objects:
            # only shape objects can have labels
            assert label != "", "label cannot be empty"
            # assert label starts with a UPPER letter
            assert label[
                0
            ].isupper(), f"label must start with an uppercase letter {label}"
            self.tokens.append(f"{label}:")

        self.tokens.append(self.object_type)

        self(*attributes)

        self.__post_init__()

    def __post_init__(self):
        pass

    def __str__(self):
        return " ".join(self.tokens)

    def text(self, *contents: str):
        """Add text to the object."""
        for cc in contents:
            self(text(cc))
        return self

    @staticmethod
    def factory(obj_type: str, label, *args, **kwargs):
        if obj_type in shape_objects:
            return Shape(obj_type, label, *args, **kwargs)
        if obj_type in line_objects:
            return Line(obj_type, label, *args, **kwargs)
        if obj_type in ctrl_objects:
            if obj_type == "var":
                return var(obj_type, label, *args, **kwargs)
            return statement(obj_type, label, *args, **kwargs)
        raise ValueError(f"Invalid object type: {obj_type}")


class Shape(PikchrObject):
    unary_annotations = ("thin", "thick", "invisible", "invis")
    binary_annotations = (
        "ht",
        "wid",
        "rad",
        "height",
        "width",
        "radius",
        "color",
        "fill",
    )

    def __post_init__(self):
        super().__post_init__()
        # add position annotation to the shape object
        positions :tuple = (
            "n",
            "north",
            "ne",
            "e",
            "east",
            "se",
            "s",
            "south",
            "sw",
            "w",
            "west",
            "nw"
        )
        for p in positions:
            setattr(self, p, f"{self}.{p}")

    def __format__(self, format_spec: str):
        """used in f-string and str.format() to refer to the object"""
        return self.label



class Line(PikchrObject):
    unary_annotations = ("thin", "thick", "invisible", "invis")
    binary_annotations = (
        "rad",
        "radius",
        "color",
        # "from", # from and to are reserved keywords
        # "to",
    )


class statement(PikchrObject):
    """statement object"""

    def __post_init__(self):
        super().__post_init__()
        # pop the first token (object type)
        self.tokens.pop(0)


class var(statement):
    """variable object"""

    def __post_init__(self):
        super().__post_init__()
        assert len(self.tokens) == 2, f"Invalid var object: {self.tokens}"
        if not self.tokens[0].startswith("$"):
            self.tokens[0] = f"${self.tokens[0]}"

    def __format__(self, format_spec: str):
        """used in f-string and str.format() to refer to the object"""
        return self.tokens[0]

    def __str__(self):
        return f"{self.tokens[0]} = {self.tokens[1]}"

    def x(self, s: str | text):
        """return an expression for `s * self`"""
        return f"{s}*{self}"
