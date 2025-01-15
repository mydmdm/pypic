from .objects import PikchrObject, create_obj, all_objects
from .utils import text


class PikchrContext:
    """Context means where user writing the diagram script in."""

    def __init__(self):
        self.sources :list[PikchrObject] = [] # lines of code (source diagram script)
        self.image_bytes :bytes = None # placeholder to save created image
        for s in all_objects():
            setattr(self, s, lambda *attributes, obj_type=s: self.new_obj(obj_type, *attributes))

    def new_obj(self, obj_type: str, *attributes: str|text, ):
        """Generate a new object id."""
        label = obj_type.upper() + str(len(self.sources))
        obj = create_obj(obj_type, label, *attributes)
        self.sources.append(obj)
        return obj

    def __str__(self):
        """Return the diagram script.
        Particularly, use ' ' to join tokens in each line and use '\n' to join lines.
        """
        return "\n".join([str(line) for line in self.sources])



