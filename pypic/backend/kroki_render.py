import base64
import zlib
import requests

from .base_render import RenderBase


class KrokiRender(RenderBase):
    """Kroki backend for PyPIC."""

    url_template = "https://kroki.io/{img_lang}/{img_format}/{img_src}"

    def script_to_bytes(self, src: str, format: str = 'svg') -> bytes:
        enc = self.encode(src)
        url = self.url_template.format(
            img_lang=self.img_lang,
            img_format=format,
            img_src=enc
        )
        response = requests.get(url)
        if response.status_code == 200:
            img_bytes = response.content
        else:
            messages = [
                'Kroki failed to render the diagram.',
                f'Status code: {response.status_code}',
                'Error message:',
            ]
            messages.extend(response.content.decode(encoding='utf-8').splitlines())
            messages.append(f'source code: {src}')
            raise RuntimeError('\n'.join(messages))
        if format == 'svg':
            return img_bytes
        else:
            raise NotImplementedError(f"Format '{format}' is not supported by Kroki backend.")

    @staticmethod
    def encode(src: str, zlib_level: int = 9) -> str:
        """Encode the source code as follows:
            str -> encode -> compress -> base64 -> ascii
        """
        return base64.urlsafe_b64encode(
            zlib.compress(
                str.encode(src), level=zlib_level
            )
        ).decode(encoding='ascii')

