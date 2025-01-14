##################################
# Pikchr Objects
# https://pikchr.org/home/doc/trunk/doc/grammar.md
##################################
from .utils import Stream


ctrl_objects: tuple[str, ...] = ('var', 'statement')
line_objects: tuple[str, ...] = ("arrow", "arc", "line", "move", "spline")
shape_objects: tuple[str, ...] = (
    "box",
    "circle",
    "cylinder",
    "diamond",
    "ellipse",
    "file",
    "oval",
)


class PikchrObject(Stream):

    def __init__(self, object_type: str, label: str = None, *attributes: str):
        super().__init__()
        self.object_type = object_type
        self.label = label

        if self.is_shape:
            # only shape objects can have labels
            self(label + ":")
        if self.is_shape or self.is_line:
            self(object_type)
        self(*attributes)

        self.__post_init__()

    @property
    def is_shape(self):
        return self.object_type in shape_objects

    @property
    def is_line(self):
        return self.object_type in line_objects

    def __post_init__(self):
        if self.is_shape:
            # verify label is valid (first letter is uppercase)
            assert self.label[0].isupper(), f"Invalid label: {self.label}"
            assert self.tokens[0] == self.label + ":", f"Invalid label: {self.label}"


class Shape(PikchrObject):
    """shape object can be referred to by its label"""

    def __format__(self, format_spec: str):
        """used in f-string and str.format() to refer to the object"""
        return self.label


class Line(PikchrObject):
    pass


class statement(PikchrObject):
    """statement object will not include the object type in the output"""
    pass


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


def all_objects() -> list[str]:
    return shape_objects + line_objects + ctrl_objects


def create_obj(obj_type: str, label, *args, **kwargs) -> PikchrObject:
    if obj_type in shape_objects:
        return Shape(obj_type, label, *args, **kwargs)
    if obj_type in line_objects:
        return Line(obj_type, label, *args, **kwargs)
    if obj_type in ctrl_objects:
        if obj_type == "var":
            return var(obj_type, label, *args, **kwargs)
        return statement(obj_type, label, *args, **kwargs)
    raise ValueError(f"Invalid object type: {obj_type}")