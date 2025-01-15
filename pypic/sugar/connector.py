"""grammar sugar for connector"""


from typing import Literal
from ..grammar.context import PikchrContext
from ..grammar.objects import Line


def connect(obj: Line,
            direction: str,
            length1: str, length2: str,
            turn_at: float = 0.5,
            ) -> None:
    """Connect two or more elements in the context
    Args:
        obj (Line): The line object (e.g., arrow) to connect the elements with.
        direction (str): The direction to connect the elements in.
            e.g., "right-up" will draw an arrow right then up
        length1 (str): The length along the first direction to draw the arrow.
        length2 (str): The length along the second direction to draw the arrow.
        turn_at (float): The point at which to turn the arrow.
    """
    d1, d2 = direction.split("-")
    return obj(
        f"{d1} {turn_at}*{length1}",
        f"then {d2}  {length2}",
        f"then {d1} (1-{turn_at})*{length1}",
    )