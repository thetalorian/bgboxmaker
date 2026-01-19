from bgboxmaker.dim import Dim
from bgboxmaker.model import FeatureType, FeatureConfig
from bgboxmaker.model import SectionConfig, SectionType
from bgboxmaker.model import Orientation
from bgboxmaker.view import BackgroundRenderer, FeatureGrid
from bgboxmaker.view.feature import PanelFeature, ImageFeature, TextFeature
from typing import Tuple, Union
from PIL import Image, ImageDraw, ImageFont, ImageColor
import logging
logger = logging.getLogger(__name__)


class Section:
    """Object representing a section of a tuck box for rendering.

    Attributes
    ----------
    pos : Dim
        The intended position of the section on the final box image.
    size : Dim
        The width and height of the section.
    rotated : bool
        If true, rotate the section by 180 degrees for the render.
    flip_h : bool
        If true, flip the image horizontally for the render.
    flip_v : bool
        If true, flip the image vertically for the render.
    type : SectionType
        The assigned type for the section, controls the shape of the render.
    cutin : int
        Sets the size of the thumb hole on the back of the tuck box.
    data : dict
        A collection of additional configuration options for this section.
    orientation: Orientation
        Working orientation to use when generating the section image.
    print_orientation : Orientation
        Final orientation of the section image when it is placed.

    Methods
    -------

    render() -> Image
        Returns an Image object containing the background and any
        requested features.

    render_mask() -> Image
        Returns an Image object containing the shape of the section
        in grayscale for use as an image mask.

    render_border(color : ImageColor, width : int) -> Image
        Returns an Image object containing the section shape,
        scaled up by width * 2, in the requested color.

        Can be combined with a mask to create an outline.
    """

    def __init__(self, config : SectionConfig):
        self.__config : SectionConfig = config
        self.__pos : Dim = Dim()
        self.__size : Dim = Dim()
        self.__rotated : bool
        if self.__config.rotated_is_set:
            self.__rotated = self.__config.rotated
        else:
            self.__rotated = False
        self.__flip_h : bool = False
        self.__flip_v : bool = False
        self.__type : SectionType = SectionType.PANE
        self.__cutin : int = 0
        self.__orientation : Orientation
        if self.__config.orientation_is_set:
            self.__orientation = self.__config.orientation
        else:
            self.__orientation : Orientation = Orientation.PORTRAIT
        self.__print_orientation : Orientation = Orientation.PORTRAIT

    @property
    def config(self) -> SectionConfig:
        return self.__config

    @property
    def pos(self) -> Dim:
        return self.__pos

    @pos.setter
    def pos(self, value: Dim):
        self.__pos = value

    @property
    def size(self) -> Dim:
        return self.__size

    @size.setter
    def size(self, value: Dim) -> None:
        self.__size = value
        self._fix_size()

    @property
    def rotated(self) -> bool:
        return self.__rotated

    @rotated.setter
    def rotated(self, value: bool) -> None:
        if not self.config.rotated_is_set:
            self.__rotated = value

    @property
    def flip_h(self) -> bool:
        return self.__flip_h

    @flip_h.setter
    def flip_h(self, value: bool) -> None:
        self.__flip_h = value

    @property
    def flip_v(self) -> bool:
        return self.__flip_v

    @flip_v.setter
    def flip_v(self, value: bool) -> None:
        self.__flip_v = value

    @property
    def type(self) -> SectionType:
        return self.__type

    @type.setter
    def type(self, value: SectionType) -> None:
        self.__type = value

    @property
    def cutin(self) -> int:
        return self.__cutin

    @cutin.setter
    def cutin(self, value: int) -> None:
        self.__cutin = value

    @property
    def orientation(self) -> Orientation:
        return self.__orientation

    @orientation.setter
    def orientation(self, value : Orientation) -> None:
        if not self.config.orientation_is_set:
            self.__orientation = value
        self._fix_size()

    @property
    def print_orientation(self) -> Orientation:
        return self.__print_orientation

    @print_orientation.setter
    def print_orientation(self, value : Orientation) -> None:
        self.__print_orientation = value


    def _fix_size(self) -> None:
        """Make sure that the height and width specification matches orientation."""
        s1 = self.__size.x
        s2 = self.__size.y
        if self.__orientation == Orientation.LANDSCAPE:
            self.__size.x = max(s1, s2)
            self.__size.y = min(s1, s2)
        if self.orientation == Orientation.PORTRAIT:
            self.__size.x = min(s1, s2)
            self.__size.y = max(s1, s2)


    def _fix_orientation(self, fixed : Image.Image) -> Image.Image:
        """Rotate or flip image as needed."""

        if self.__orientation != self.__print_orientation:
            fixed = fixed.rotate(90, expand=1)

        if self.__rotated:
            fixed = fixed.rotate(180)

        if self.__flip_v:
            fixed = fixed.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        if self.__flip_h:
            fixed = fixed.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        return fixed


    def _draw_shapes(self, mode : str, size : Dim, back : str, fill : str) -> Image.Image:
        """Draw the shape of the section in the requested color"""
        image = Image.new(mode, size.wh, back)
        draw = ImageDraw.Draw(image, mode)

        if self.type in [SectionType.PANE, SectionType.GLUE_TAB]:
            draw.rectangle((0, 0, size.x, size.y), fill=fill, width=0)

        if self.type == SectionType.SIDE_TAB:
            # For the side tabs we need a polygon
            # mask to cut out the correct shape.
            p1 = (0, size.y)
            p2 = (0, size.y / 2)
            p3 = (size.x / 4, 0)
            p4 = (size.x, 0)
            p5 = (size.x, size.y)
            draw.polygon([p1, p2, p3, p4, p5], fill=fill, width=0)

        if self.type == SectionType.TUCK_TAB:
            # Tuck tab should be rounded at the bottom.
            w = int(size.x)
            h = int(size.y / 2)
            draw.pieslice((0, 0, w, 2 * h), 0, 180, fill=fill, width=0)
            draw.rectangle((0, 0, w, h), fill=fill, width=0)

        if self.type == SectionType.BACK:
            draw.rectangle((0, 0, size.x, size.y), fill=fill, width=0)

            w = int(self.__cutin)
            h = int(self.__cutin / 2)
            x = int(size.x / 2 - self.__cutin / 2)
            y = int(-self.__cutin / 4)
            draw.ellipse((x, y, x + w, y + h), fill=back, width=0)

        return image


    def _get_border(self, color, width) -> Image.Image:
        """Draw the shape of the section scaled up to create a border."""
        border_size = Dim(self.__size.x + width * 2, self.__size.y + width * 2)
        border = self._draw_shapes("RGBA", border_size, "#00000000", color)
        return border


    def _get_mask(self) -> Image.Image:
        """Draw the shape of the section for use as an alpha mask."""
        mask = self._draw_shapes("L", self.size, "white", "black")
        return mask


    def _get_margin(self) -> int:
        """Calculate actual margin in pixels"""
        # Get margin in pixels
        margin = int(self.config.common.margin * self.config.common.resolution)

        # Reduce margin if section is too small,
        # leave at least 10px usable space if possible
        while margin > 0:
            used = (margin * 2) + 10
            if self.__size.x >= used and self.__size.y >= used:
                break
            margin -= 1

        return margin

    def _get_hard_bounds(self, margin : int) -> Dim:
        """Calculate hard boundaries for this section based on margin."""

        # Calculate bounds
        bounds : Dim = Dim(self.size.x - 2 * margin, self.size.y - 2 * margin)
        return bounds

    def _get_feature_bounds(self, config : FeatureConfig, hard_bounds : Dim) -> Dim:
        """Calculate feature bounds"""
        feature_bounds = hard_bounds
        request : Dim = Dim(config.width, config.height)
        request = (request * config.common.resolution).as_ints()

        if request.w > 0 and request.h > 0:
            # If width and height are specified that sets the aspect ratio for the bounds.
            if request.w > hard_bounds.w or request.h > hard_bounds.h:
                # Requested bounds needs to be resized to fit in hard bounds, while keeping
                # requested aspect ratio.
                feature_ratio : float = request.w / request.h
                bounds_ratio : float = hard_bounds.w / hard_bounds.h

                if feature_ratio < bounds_ratio:
                    # Adjust width
                    feature_bounds.w = int(hard_bounds.h * feature_ratio)
                else:
                    # Adjust height
                    feature_bounds.h = int(hard_bounds.w / feature_ratio)
            else:
                # Requested bounds fits within hard bounds and can be used directly.
                feature_bounds.w = request.w
                feature_bounds.h = request.h
        elif config.width > 0:
            # If only width is specified, check if it fits within the hard bounds
            if request.w < hard_bounds.x:
                hard_bounds.w = request.w
            else:
                logger.warning(f"Requested width for feature {config.type} larger than hard boundary.")
        elif config.height > 0:
            # If only height is specified, check if it fits within the hard bounds.
            if request.h < hard_bounds.h:
                hard_bounds.h = request.h
            else:
                logger.warning(f"Requested width for feature {config.type} larger than hard boundary.")

        return feature_bounds

    def _get_features(self) -> Image.Image:
        """Render the requested features on the section."""
        feature_layer : Image.Image = Image.new("RGBA", self.size.wh, (0,0,0,0))

        # Get margin
        margin : int = self._get_margin()

        # Get hard bounds
        bounds : Dim = self._get_hard_bounds(margin)

        # Set up feature grid
        grid : FeatureGrid = FeatureGrid(self.config.grid, self.size, margin)

        # Render individual features
        for feature in self.config.features:
            # Set feature location
            # ---

            # Get position
            pos : Dim = grid.get_pos(feature.place)

            # Calculate feature bounds
            feature_bounds = self._get_feature_bounds(feature, bounds)

            # Generate feature image
            feature_object = self._feature_factory(feature)
            feature_image : Image.Image = feature_object.render(feature_bounds)
            fw, fh = feature_image.size

            pos.x = pos.x - (feature.anchor.x * int(fw / 2))
            pos.y = pos.y - (feature.anchor.y * int(fh / 2))


            # TODO: Adjust for possible out of bounds with anchor position
            feature_layer.alpha_composite(feature_image, pos.xy)

        return feature_layer

    def _feature_factory(self, config : FeatureConfig):
            if config.type == FeatureType.PANEL:
                return PanelFeature(config)
            elif config.type == FeatureType.TEXT:
                return TextFeature(config)
            elif config.type == FeatureType.IMAGE:
                return ImageFeature(config)


    def render(self) -> Image.Image:
        """Render the full section with background and features."""
        # Create Section Image
        render = Image.new("RGBA", self.size.wh, (0,0,0,0))
        mask = self._get_mask()

        # Render background
        bg_renderer = BackgroundRenderer(self.config.background)
        background = bg_renderer.render(self.size)
        render = Image.composite(render, background, mask)

        if len(self.config.features) > 0:
            features = self._get_features()
            render = Image.composite(render, features, mask)

        render = self._fix_orientation(render)
        return render


    def render_mask(self) -> Image.Image:
        """Render the section as an alpha mask."""
        mask = self._get_mask()
        mask = self._fix_orientation(mask)
        return mask


    def render_border(self, color : str, width : int) -> Image.Image:
        """Render the section scaled up as a border."""
        border = self._get_border(color, width)
        border = self._fix_orientation(border)
        return border

    def __repr__(self) -> str:
        attributes : list[str] = []
        attributes.append(f"Config:\n{self.__config}")
        attributes.append(f"pos: {self.__pos}")
        attributes.append(f"size: {self.__size}")
        attributes.append(f"rotated: {self.__rotated}")
        attributes.append(f"flip_h: {self.__flip_h}")
        attributes.append(f"flip_v: {self.__flip_v}")
        attributes.append(f"type: {self.__type}")
        attributes.append(f"cutin: {self.__cutin}")
        attributes.append(f"orientation: {self.__orientation}")
        attributes.append(f"print orientation: {self.__print_orientation}")
        return "\n".join(attributes)