from bgboxmaker import FeatureConfig, Dim, FontConfig, OptionsTextConfig
from bgboxmaker.view.feature import Feature
from PIL import Image, ImageDraw, ImageFont


class TextFeature(Feature):
    """Create text to add to a box section."""

    def __init__(self, config : FeatureConfig):
        self.config = config

    def render(self, bounds : Dim) -> Image.Image:
        """Render text to fit in requested bounds."""

        # Extract options
        options : OptionsTextConfig = self.config.options # type: ignore

        # Create initial canvas
        render = Image.new("RGBA", (bounds.w, bounds.h), (0,0,0,0))
        draw = ImageDraw.Draw(render)

        # Get text anchor
        h_anchor = ['l', 'm', 'r']
        v_anchor = ['a', 'm', 'd']
        t_anchor = "{}{}".format(h_anchor[self.config.anchor.x], v_anchor[self.config.anchor.y])

        # Get position
        pos = Dim(0,0)
        pos.x = self.config.anchor.x * int(bounds.w / 2)
        pos.y = self.config.anchor.y * int(bounds.h / 2)

        # # Find appropriate font size
        font_data : FontConfig = options.common.font
        font_size = font_data.size

        while font_size > 8:
            # Set font
            font = ImageFont.truetype(font_data.name, font_size)
            # Get Bounding Box size
            tx1, ty1, tx2, ty2 = draw.multiline_textbbox((0,0), options.text, font=font, anchor=t_anchor, align=options.align, stroke_width=font_data.width)
            w = tx2 - tx1
            h = ty2 - ty1

            if w < bounds.x and h < bounds.y:
                break

            font_size = font_size - 1

        font = ImageFont.truetype(font_data.name, font_size)
        draw.multiline_text(pos.xy, options.text, font=font, anchor=t_anchor, align=options.align, stroke_width=font_data.width, fill=font_data.color, stroke_fill=font_data.stroke)

        return render
