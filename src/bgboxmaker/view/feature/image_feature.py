from bgboxmaker import FeatureConfig, Dim
from bgboxmaker.view.feature import Feature
from PIL import Image


class ImageFeature(Feature):
    """Creates an image to add to a box section."""

    def __init__(self, config : FeatureConfig):
        self.config : FeatureConfig = config

    def _get_image(self, filename : str) -> Image.Image:
        """Open and return an Image"""
        with Image.open(filename, 'r') as im:
            return im


    def render(self,  bounds : Dim) -> Image.Image:
        """Render an image at the expected size."""

        # Retrieve the image
        image = self._get_image(self.config.options.image_path) # type: ignore

        # Resize to spec
        image_size : Dim = Dim()
        image_size.w, image_size.h = image.size


        if self.config.width > 0 and self.config.height > 0:
            # If both width and height are given in the config,
            # we are changing aspect: resize directly to bounds
            render = image.resize([bounds.w, bounds.y])
        else:
            # Otherwise, we need to keep the image's original aspect ratio,
            # resized to fit within the bounds.
            image_ratio : float = image_size.w / image_size.h
            bounds_ratio : float = bounds.w / bounds.h

            if image_ratio < bounds_ratio:
                image_size.w = int(bounds.h * image_ratio)
                image_size.h = bounds.h
            else:
                image_size.w = bounds.w
                image_size.h = int(bounds.w / image_ratio)

            render = image.resize([image_size.w, image_size.h])

        return render
