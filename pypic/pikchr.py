from .grammar.context import PikchrContext
from .backend import RenderPipeline, KrokiRender, RenderBase, ipython_display_image
from .utils import FileWriter


class pikchr:
    """context manager for PikchrContext
    Example:
    ```
    with pikchr(show=True) as ctx:
        ctx("box \"Hello, Pikchr!\"")
    ```
    """

    def __init__(
        self, /,
        print_script: bool = True,  # print the script after exiting the context
        display_image: bool = False,  # show the diagram after exiting the context
        output_prefix: str = None,  # prefix to save output
        output_format: str = "svg",  # output format for the diagram
        render: RenderBase = None,  # render function to use
    ):
        self.context = PikchrContext()
        self.pipeline = RenderPipeline(render or KrokiRender())
        if display_image:
            self.pipeline.image_bytes_hooks.append(ipython_display_image)
        if print_script:
            self.pipeline.script_hooks.append(print)
        if output_prefix:
            script_file = FileWriter(f"{output_prefix}.pikchr", "w")
            self.pipeline.script_hooks.append(script_file.write)
            img_file = FileWriter(f"{output_prefix}.{output_format}", "wb")
            self.pipeline.image_bytes_hooks.append(img_file.write)


    def __enter__(self):
        return self.context

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.context.image_bytes = self.pipeline(str(self.context))
        except Exception as e:
            print(e)

