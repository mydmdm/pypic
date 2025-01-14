from .kroki_render import KrokiRender
from .base_render import RenderBase


supported_renders = {
    'kroki': KrokiRender,
}


def get_render(name: str, params: dict = None) -> RenderBase:
    """Get a renderer by name."""
    name = name.lower()
    assert name in supported_renders, f"Render '{name}' is not supported ({list(supported_renders.key())})."
    params = params or {}
    return supported_renders[name](**params)