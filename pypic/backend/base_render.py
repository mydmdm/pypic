"""Base classes for Pikchr rendering."""


class RenderBase:
    """Base class for rendering."""

    img_lang: str = 'pikchr'

    def __init__(self):
        self.img_source :str = None
        self.img_bytes :bytes = None
        self.img_format :str = 'svg'

    def __call__(self, src: str, format: str = 'svg', show: bool = False) -> bytes:
        self.img_source = src
        self.img_format = format
        self.img_bytes = self.script_to_bytes(src, format)
        if show:
            self.show()
        return self.img_bytes

    def show(self):
        from IPython.display import SVG, display
        if self.img_format == 'svg':
            display(SVG(self.img_bytes))

    @classmethod
    def script_to_bytes(cls, src: str, format: str = 'svg') -> bytes:
        raise NotImplementedError("Method 'render' must be implemented in subclasses.")
