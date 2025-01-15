import base64
import zlib
import requests

from .pipeline import RenderBase


class KrokiRender(RenderBase):
    """Kroki backend for PyPIC."""
    supported_output_formats = ('svg',)

    url_template = "https://kroki.io/pikchr/{output_format}/{img_src}"

    def __init__(self, compress_level: int = 9):
        super().__init__()
        self.compress_level = compress_level

    def create_image(self, src: str, output_format: str = 'svg') -> bytes:
        """Render Pikchr code using Kroki backend."""
        if output_format not in self.supported_output_formats:
            raise ValueError(f"Format '{output_format}' is not supported by Kroki backend.")

        enc = self.encode(src)
        url = self.url_template.format(
            img_src=enc,
            output_format=output_format,
        )

        response = requests.get(url)
        if response.status_code == 200:
            img_bytes = response.content
            return img_bytes
        else:
            messages = [
                'Kroki failed to render the diagram.',
                f'Status code: {response.status_code}',
                'Error message:',
            ]
            messages.extend(response.content.decode(encoding='utf-8').splitlines())
            # messages.append(f'source code: {src}')
            raise RuntimeError('\n'.join(messages))

    def encode(self, src: str) -> str:
        """Encode the source code as follows:
            str -> encode -> compress -> base64 -> ascii
        """
        if self.compress_level == 0:
            # skip compression
            return base64.urlsafe_b64encode(
                str.encode(src)
            ).decode(encoding='ascii')

        return base64.urlsafe_b64encode(
            zlib.compress(
                str.encode(src), level=self.compress_level
            )
        ).decode(encoding='ascii')

