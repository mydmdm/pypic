"""Base classes for Pikchr rendering."""
from ..utils import safe_open
import os

class RenderBase:
    """Base class for rendering."""

    img_lang: str = 'pikchr'

    def __init__(self, /,
                 output_format: str = 'svg',
                 output_prefix: str = None,
                 ):
        self.output_format = output_format
        self.output_prefix = output_prefix

        self.img_source :str = None
        self.img_bytes :bytes = None

    def __call__(self, src: str) -> bytes:
        self.img_source = src
        if self.output_prefix is not None:
            with safe_open(self.output_prefix + ".pikchr", 'w') as f:
                f.write(src)

        self.img_bytes = self.script_to_bytes(src, format)

        if self.img_bytes is not None and self.image_output is not None:
            with safe_open(f"{self.output_prefix}.{self.output_format}", 'wb') as f:
                f.write(self.img_bytes)

        return self.img_bytes

    def show_image(self):
        """Display the image (for notebook environment)."""
        from IPython.display import SVG, display, Image

        if self.img_bytes is None:
            return

        if self.img_format == 'svg':
            display(SVG(self.img_bytes))
        else:
            display(Image(data=self.img_bytes))

    @classmethod
    def script_to_bytes(cls, src: str, format: str = 'svg') -> bytes:
        return None
