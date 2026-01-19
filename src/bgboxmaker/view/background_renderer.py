from bgboxmaker.dim import Dim
from bgboxmaker.model import BackgroundConfig
from PIL import Image, ImageDraw

class BackgroundRenderer:
    """Create a background image for a box or section."""

    def __init__(self, config : BackgroundConfig):
        self.config : BackgroundConfig = config

    def _get_image(self, filename : str) -> Image.Image:
        """Open and return an Image"""
        with Image.open(filename, 'r') as im:
            return im


    def render(self, bounds : Dim) -> Image.Image:
        """Render the background image or color to the size of the bounding box."""
        background = Image.new("RGBA", bounds.wh, (0,0,0,0))

        if self.config.image:
            # Load Background image
            bg_image = self._get_image(self.config.image_path)
            bgw, bgh = bg_image.size

            bg_ratio = float(bgw) / bgh
            bounds_ratio = float(bounds.x) / bounds.y

            # Resize background to fit smallest bounds while keeping aspect
            if bg_ratio < bounds_ratio:
                # Match the width to cover the whole area.
                bgw = bounds.x
                bgh = int(bounds.x / bg_ratio)
            else:
                # Match the height to cover the whole area.
                bgh = bounds.y
                bgw = int(bounds.y * bg_ratio)
            bg_image = bg_image.resize((bgw, bgh))

            # Crop background to fit bounds
            crop_pos = Dim(0, 0)
            if bgw > bounds.x:
                delta = bgw - bounds.x
                crop_pos.x = int(delta / 2)
            if bgh > bounds.y:
                delta = bgh - bounds.y
                crop_pos.y = int(delta / 2)
            bg_image = bg_image.crop((crop_pos.x, crop_pos.y, crop_pos.x + bounds.x, crop_pos.y + bounds.y))
            background.paste(bg_image)
        elif self.config.color:
            background_draw = ImageDraw.Draw(background)
            background_draw.rectangle((0,0,bounds.x,bounds.y), fill=self.config.color, width=0)

        return background
