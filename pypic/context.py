from functools import partial
from .backend import RenderBase, get_render
from .objects import text, PikchrObject, shape_objects, line_objects, ctrl_objects


class PikchrContext:
    """Context means where user writing the diagram script in."""

    def __init__(self):
        self.sources :list[PikchrObject] = [] # lines of code (source diagram script)

        for s in shape_objects + line_objects + ctrl_objects:
            setattr(self, s, lambda *attributes, obj_type=s: self.new_obj(obj_type, *attributes))

    def new_obj(self, obj_type: str, *attributes: str|text, ):
        """Generate a new object id."""
        label = obj_type.upper() + str(len(self.sources))
        obj = PikchrObject.factory(obj_type, label, *attributes)
        self.sources.append(obj)
        return obj

    def __str__(self):
        """Return the diagram script.
        Particularly, use ' ' to join tokens in each line and use '\n' to join lines.
        """
        return "\n".join([str(line) for line in self.sources])

    # def batch_create(self, obj_types: str|list,  obj_cfgs: list[tuple], stride: str):
    #     """Create multiple objects at once, each object is defined by a dictionary.
    #     Each object is separated by a stride."""
    #     if isinstance(obj_types, str):
    #         obj_types = [obj_types] * len(obj_cfgs)

    #     objects = [None] * len(obj_cfgs)
    #     for cfg in obj_cfgs:
    #         self.new_obj(cfg.pop("type"), *cfg.values())


class pikchr:
    """context manager for PikchrContext
    Example:
    ```
    with pikchr(show=True) as ctx:
        ctx("box \"Hello, Pikchr!\"")
    ```
    """

    def __init__(self, render: str = 'kroki',
                render_params: dict = None,
                show: bool = False, # show the diagram after exiting the context
                ):
        self.context = PikchrContext()
        self.show_diagram = show
        if render is not None:
            self.render = get_render(render, render_params)
        else:
            self.render = None

    def __enter__(self):
        return self.context

    def __exit__(self, exc_type, exc_value, traceback):
        if self.show_diagram:
            src_code = str(self.context)
            if self.render is not None:
                try:
                    self.render(src_code, show=True)
                except Exception as e:
                    print(str(e))
            else:
                print(src_code)
