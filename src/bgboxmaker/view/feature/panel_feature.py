from bgboxmaker import FeatureConfig, Dim
from bgboxmaker.view.feature import Feature
from PIL import Image, ImageDraw


class PanelFeature(Feature):
    """Creates a panel to add to a box section."""

    def __init__(self, config : FeatureConfig):
        self.config = config

    def render(self, bounds : Dim) -> Image.Image:
        """Render a panel at requested size, with requested border."""
        color : str = self.config.options.color # type: ignore
        border : str = self.config.options.border # type: ignore
        width : int = self.config.options.border_width # type: ignore

        panel = Image.new("RGBA", (bounds.w, bounds.h), color)

        if width > 0:
            draw = ImageDraw.Draw(panel, "RGBA")
            draw.rectangle((0, 0, bounds.w, bounds.h), fill=color, outline=border, width=width)

        return panel
