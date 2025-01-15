"""a hello world test"""
import pytest
import re

from pypic import pikchr, RenderBase, text


reference_script = """\
arrow right 200% "Markdown" "Source"
box rad 10px "Markdown" "Formatter" "(markdown.c)" fit
arrow right 200% "HTML+SVG" "Output"
arrow <-> down 70% from last box.s
box same "Pikchr" "Formatter" "(pikchr.c)" fit\
"""

svg_rendered = b"""<svg xmlns='http://www.w3.org/2000/svg' style='font-size:initial;' viewBox="0 0 423.821 217.44">
<polygon points="146.16,37.44 134.64,41.76 134.64,33.12" style="fill:rgb(0,0,0)"/>
<path d="M2.16,37.44L140.4,37.44"  style="fill:none;stroke-width:2.16;stroke:rgb(0,0,0);" />
<text x="74.16" y="25.74" text-anchor="middle" fill="rgb(0,0,0)" dominant-baseline="central">Markdown</text>
<text x="74.16" y="49.14" text-anchor="middle" fill="rgb(0,0,0)" dominant-baseline="central">Source</text>
<path d="M161.16,72.72L258.341,72.72A15 15 0 0 0 273.341 57.72L273.341,17.16A15 15 0 0 0 258.341 2.16L161.16,2.16A15 15 0 0 0 146.16 17.16L146.16,57.72A15 15 0 0 0 161.16 72.72Z"  style="fill:none;stroke-width:2.16;stroke:rgb(0,0,0);" />
<text x="209.75" y="17.28" text-anchor="middle" fill="rgb(0,0,0)" dominant-baseline="central">Markdown</text>
<text x="209.75" y="37.44" text-anchor="middle" fill="rgb(0,0,0)" dominant-baseline="central">Formatter</text>
<text x="209.75" y="57.6" text-anchor="middle" fill="rgb(0,0,0)" dominant-baseline="central">(markdown.c)</text>
<polygon points="417.341,37.44 405.821,41.76 405.821,33.12" style="fill:rgb(0,0,0)"/>
<path d="M273.341,37.44L411.581,37.44"  style="fill:none;stroke-width:2.16;stroke:rgb(0,0,0);" />
<text x="345.341" y="25.74" text-anchor="middle" fill="rgb(0,0,0)" dominant-baseline="central">HTML+SVG</text>
<text x="345.341" y="49.14" text-anchor="middle" fill="rgb(0,0,0)" dominant-baseline="central">Output</text>
<polygon points="209.75,72.72 214.07,84.24 205.43,84.24" style="fill:rgb(0,0,0)"/>
<polygon points="209.75,144.72 205.43,133.2 214.07,133.2" style="fill:rgb(0,0,0)"/>
<path d="M209.75,78.48L209.75,138.96"  style="fill:none;stroke-width:2.16;stroke:rgb(0,0,0);" />
<path d="M176.136,215.28L243.365,215.28A15 15 0 0 0 258.365 200.28L258.365,159.72A15 15 0 0 0 243.365 144.72L176.136,144.72A15 15 0 0 0 161.136 159.72L161.136,200.28A15 15 0 0 0 176.136 215.28Z"  style="fill:none;stroke-width:2.16;stroke:rgb(0,0,0);" />
<text x="209.75" y="159.84" text-anchor="middle" fill="rgb(0,0,0)" dominant-baseline="central">Pikchr</text>
<text x="209.75" y="180" text-anchor="middle" fill="rgb(0,0,0)" dominant-baseline="central">Formatter</text>
<text x="209.75" y="200.16" text-anchor="middle" fill="rgb(0,0,0)" dominant-baseline="central">(pikchr.c)</text>
</svg>"""


class MockRender(RenderBase):

    @classmethod
    def create_image(cls, src, output_format = 'svg'):
        print("working in a mock render service")
        return svg_rendered


def test_hello_world():
    with pikchr(
        output_prefix="build/hello_world",
        # display_image=True,
        render=MockRender(),
    ) as p:
        p.arrow("right 200%", text("Markdown"), text("Source"))
        p.box("rad 10px", text("Markdown"), text("Formatter", "(markdown.c)"), "fit")
        p.arrow("right 200%", text("HTML+SVG"), text("Output"))
        p.arrow("<-> down 70% from last box.s")
        p.box("same", text("Pikchr"), text("Formatter", "(pikchr.c)"), "fit")

    script = str(p)
    # remove the label (^\w:) from the script with re
    script = re.sub(r"^[A-Za-z0-9]+: ", "", script, flags=re.MULTILINE)
    assert script == reference_script

    with open("build/hello_world.pikchr", "r") as f:
        assert str(p) == f.read()

    with open("build/hello_world.svg", "rb") as f:
        data = f.read()
        assert data == svg_rendered
        assert p.image_bytes == data
