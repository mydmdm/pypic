"""Base classes for Pikchr rendering."""


class RenderBase:
    supported_output_formats :tuple = None

    @classmethod
    def create_image(cls, src: str, output_format: str = 'svg') -> bytes:
        raise NotImplementedError


class RenderPipeline:
    """A pipeline for rendering Pikchr scripts."""

    def __init__(self, render: RenderBase):
        self.render = render
        self.script_hooks = []
        self.image_bytes_hooks = []

    def __call__(self, src: str, output_format: str = 'svg') -> bytes:
        for hook in self.script_hooks:
            hook(src)
        if self.render is not None:
            img_bytes = self.render.create_image(src, output_format)
            for hook in self.image_bytes_hooks:
                hook(img_bytes)
            return img_bytes
        return None


def ipython_display_image(self):
    """Display the image (for notebook environment)."""
    from IPython.display import SVG, display, Image

    if self.img_bytes is None:
        return

    if self.img_format == 'svg':
        display(SVG(self.img_bytes))
    else:
        display(Image(data=self.img_bytes))

