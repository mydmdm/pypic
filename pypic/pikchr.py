from .grammer.context import PikchrContext
from .backend import get_render, RenderBase


class pikchr:
    """context manager for PikchrContext
    Example:
    ```
    with pikchr(show=True) as ctx:
        ctx("box \"Hello, Pikchr!\"")
    ```
    """

    def __init__(
        self,
        render: RenderBase = None,  # render object
        show_image: bool = False,  # show the diagram after exiting the context
    ):
        self.context = PikchrContext()
        self.render = render
        self.show_diagram = show_image

    def __enter__(self):
        return self.context

    def __exit__(self, exc_type, exc_value, traceback):
        if self.render is not None:
            self.render(str(self.context))
        if self.show_diagram:
            src_code = str(self.context)
            if self.render is not None:
                try:
                    self.render(src_code, show=True)
                except Exception as e:
                    print(str(e))
            else:
                print(src_code)
