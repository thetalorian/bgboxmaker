from PIL import Image, ImageDraw
from bgboxmaker.dim import Dim
from bgboxmaker.model import BoxConfig, SectionConfig, SectionName, SectionType, Orientation
from bgboxmaker.view import Section, BackgroundRenderer
import logging
logger = logging.getLogger(__name__)


class Box:
    """Object representing the configuration for a tuck box.

    Provides all of the configuration options available to customize
    the look of the generated tuck box, and the generate method to
    render it as an image.

    Attributes
    ----------
    data : dict
        The configuration dictionary, loaded from provided YAML file.

    page_margin : float
        Margin required for intended printer. Given in units defined by resolution.

    page_thickness : int
        Estimate of page thickness, used to inset the tabs for easier closing.
        Given in pixels.

    resolution : int
        Pixels per Metric for the image. Sets units used for other settings.

    page : Vec2
        Holds size of full image, set to the desired page size minus the margins.

    dim : Vec3
        Pixel dimensions for the box

    tabs : Vec2
        Pixel dimensions for the box tabs (glue tab width, top and bottom tab height)
        These are the only two sections who's size is not fixed by the other dimensions.

    pos : Vec2
        Position of the actual box image on the page.

    size : Vec2
        Size of the full box image.

    font : dict
        Dictionary of font settings to use for the box
        Members :
          name: Name of the font file to use.
          size: Starting font size.
          color: Font color.
          stroke: Stroke color.
          width: Stroke width.

    Methods
    -------

    generate() -> None
        Generates the page with the box image and displays it as a preview to save or print.

    """
    def __init__(self, config : BoxConfig):
        self.__config : BoxConfig = config
        self.__sections : dict = {}
        self.__page : Dim = Dim()
        self.__dim : Dim = Dim()
        self.__tabs : Dim = Dim()
        self.__pos : Dim = Dim()
        self.__size : Dim = Dim()

        # Configure box info from config.
        self._set_page()
        self._set_box_dimensions()
        self._set_box_size()
        self._set_box_position()

        if not self._box_fits_page():
            msg = "Requested box is too big for the defined page. Adjust requested sizes to fit."
            logger.error(msg)
            raise Exception(msg)

        self._create_sections()

    @property
    def sections(self) -> dict:
        return self.__sections

    @property
    def page(self) -> Dim:
        return self.__page

    @property
    def dim(self) -> Dim:
        return self.__dim

    @property
    def tabs(self) -> Dim:
        return self.__tabs

    @property
    def pos(self) -> Dim:
        return self.__pos

    @property
    def size(self) -> Dim:
        return self.__size


    def _set_page(self) -> None:
        """Set printable page size."""
        page = self.__config.page
        resolution = self.__config.common.resolution
        self.__page.x = int((page.width - page.margin) * resolution)
        self.__page.y = int((page.height - page.margin) * resolution)


    def _set_box_dimensions(self) -> None:
        """Set box dimensions"""
        page = self.__config.page
        dim = self.__config.dimensions
        resolution = self.__config.common.resolution

        # Set box side widths in pixels
        self.__dim.x = int(dim.width * resolution + page.thickness)
        self.__dim.y = int(dim.height * resolution + page.thickness)
        self.__dim.z = int(dim.depth * resolution + page.thickness)

        # Set pixel width of glue tab
        self.__tabs.x = self.__dim.z - 20

        # Set pixel height of tuck tabs
        self.__tabs.y = int(resolution * 3 / 4)


    def _set_box_size(self) -> None:
        """Calculate pixel size of unfolded box."""
        # Width - Glue tab, left and right sides, front and back
        self.__size.x = (self.__tabs.x + (2 * self.__dim.z) + (2 * self.__dim.x))
        # Height - Top and bottom tabs, top and bottom, front / back
        self.__size.y = ((2 * self.__tabs.y) + (2 * self.__dim.z) + self.__dim.y)


    def _set_box_position(self) -> None:
        """Calculate box position on page."""
        self.__pos.x = int((self.__page.x - self.__size.x) / 2)
        self.__pos.y = int((self.__page.y - self.__size.y) / 2)


    def _box_fits_page(self) -> bool:
        """Validate that calculated box size fits on page."""
        return self.__size.x < self.__page.x and self.__size.y < self.__page.y

    def _get_section_config(self, section : SectionName) -> SectionConfig:
        detail = self.__config.detail
        if section in detail:
            return detail[section]
        elif section in [SectionName.LEFT, SectionName.RIGHT] and SectionName.SIDES in detail:
            return detail[SectionName.SIDES]
        elif section in [SectionName.TOP, SectionName.BOTTOM] and SectionName.ENDS in detail:
            return detail[SectionName.ENDS]
        elif section in [SectionName.FRONT, SectionName.BACK] and SectionName.FACES in detail:
            return detail[SectionName.FACES]
        else:
            return SectionConfig(self.__config.common)


    def _create_sections(self):
        """Generate and place sections"""

        # Reassign values for readability.
        tab = self.__tabs
        dim = self.__dim
        o = self.__config.page.thickness

        glue_tab = Section(self._get_section_config(SectionName.GLUE_TAB))
        glue_tab.pos = Dim(0, tab.y + dim.z)
        glue_tab.size = Dim(tab.x, dim.y)
        glue_tab.type = SectionType.GLUE_TAB
        self.__sections[SectionName.GLUE_TAB] = glue_tab

        back = Section(self._get_section_config(SectionName.BACK))
        back.pos = Dim(tab.x, tab.y + dim.z)
        back.size = Dim(dim.x, dim.y)
        back.cutin = tab.y
        back.type = SectionType.BACK
        self.__sections[SectionName.BACK] = back

        left = Section(self._get_section_config(SectionName.LEFT))
        left.pos = Dim(tab.x + dim.x, tab.y + dim.z)
        left.size = Dim(dim.y, dim.z)
        left.rotated = True
        left.orientation = Orientation.LANDSCAPE
        self.__sections[SectionName.LEFT] = left

        front = Section(self._get_section_config(SectionName.FRONT))
        front.pos = Dim(tab.x + dim.x + dim.z, tab.y + dim.z)
        front.size = Dim(dim.x, dim.y)
        self.__sections[SectionName.FRONT] = front

        right = Section(self._get_section_config(SectionName.RIGHT))
        right.pos = Dim(tab.x + dim.x + dim.z + dim.x, tab.y + dim.z)
        right.size = Dim(dim.y, dim.z)
        right.orientation = Orientation.LANDSCAPE
        self.__sections[SectionName.RIGHT] = right

        bottom = Section(self._get_section_config(SectionName.BOTTOM))
        bottom.pos = Dim(tab.x, tab.y + dim.z + dim.y)
        bottom.size = Dim(dim.x, dim.z)
        bottom.rotated = True
        bottom.orientation = Orientation.LANDSCAPE
        bottom.print_orientation = Orientation.LANDSCAPE
        self.__sections[SectionName.BOTTOM] = bottom

        bottom_tab = Section(self._get_section_config(SectionName.BOTTOM_TAB))
        bottom_tab.pos = Dim(tab.x + o, tab.y + dim.z + dim.y + dim.z)
        bottom_tab.size = Dim(dim.x - o * 2, tab.y)
        bottom_tab.type = SectionType.TUCK_TAB
        bottom_tab.orientation = Orientation.LANDSCAPE
        bottom_tab.print_orientation = Orientation.LANDSCAPE
        self.__sections[SectionName.BOTTOM_TAB] = bottom_tab

        top = Section(self._get_section_config(SectionName.TOP))
        top.pos = Dim(tab.x + dim.x + dim.z, tab.y)
        top.size = Dim(dim.x, dim.z)
        top.rotated = True
        top.orientation = Orientation.LANDSCAPE
        top.print_orientation = Orientation.LANDSCAPE
        self.__sections[SectionName.TOP] = top

        top_tab = Section(self._get_section_config(SectionName.TOP_TAB))
        top_tab.pos = Dim(tab.x + dim.x + dim.z + o, 0)
        top_tab.size = Dim(dim.x - o * 2, tab.y)
        top_tab.type = SectionType.TUCK_TAB
        top_tab.rotated = True
        top_tab.orientation = Orientation.LANDSCAPE
        top_tab.print_orientation = Orientation.LANDSCAPE
        self.__sections[SectionName.TOP_TAB] = top_tab

        lt_tab = Section(self._get_section_config(SectionName.LT_TAB))
        lt_tab.pos = Dim(tab.x + dim.x + o , tab.y)
        lt_tab.size = Dim(dim.z - o * 2, dim.z)
        lt_tab.type = SectionType.SIDE_TAB
        self.__sections[SectionName.LT_TAB] = lt_tab

        rt_tab = Section(self._get_section_config(SectionName.RT_TAB))
        rt_tab.pos = Dim(tab.x + dim.x + dim.z + dim.x + o, tab.y)
        rt_tab.size = Dim(dim.z - o * 2, dim.z)
        rt_tab.type = SectionType.SIDE_TAB
        rt_tab.flip_h = True
        self.__sections[SectionName.RT_TAB] = rt_tab

        lb_tab = Section(self._get_section_config(SectionName.LB_TAB))
        lb_tab.pos = Dim(tab.x + dim.x + o, tab.y + dim.z + dim.y)
        lb_tab.size = Dim(dim.z - o * 2, dim.z)
        lb_tab.type = SectionType.SIDE_TAB
        lb_tab.flip_v = True
        self.__sections[SectionName.LB_TAB] = lb_tab

        rb_tab = Section(self._get_section_config(SectionName.RB_TAB))
        rb_tab.pos = Dim(tab.x + dim.x + dim.z + dim.x + o, tab.y + dim.z + dim.y)
        rb_tab.size = Dim(dim.z - o * 2, dim.z)
        rb_tab.type = SectionType.SIDE_TAB
        rb_tab.flip_h = True
        rb_tab.flip_v = True
        self.__sections[SectionName.RB_TAB] = rb_tab


    def generate(self):
        """Generate tuck box image."""
        # Create page
        page : Image.Image = Image.new("RGBA", self.page.wh, (0,0,0,0))

        # Generate mask
        mask : Image.Image = Image.new("L", self.page.wh, "white")
        for section in self.__sections:
            section_mask = self.__sections[section].render_mask()
            pos = self.__sections[section].pos
            mask.paste(section_mask, (pos.x + self.__pos.x, pos.y + self.__pos.y))

        # Generate background
        if self.__config.background.isSet:
            # Background is slightly smaller than box to avoid printing
            # too much on the glue strip, since it won't be seen.
            inset = self.__tabs.x - 50
            bg_size : Dim = Dim(self.__size.x - inset, self.__size.y)
            bg_layer : Image.Image = Image.new("RGBA", self.page.wh, (0,0,0,0))
            background : Image.Image = BackgroundRenderer.render(self.__config.background, bg_size)
            bg_layer.paste(background, (self.__pos.x + inset, self.__pos.y))
            page = Image.composite(page, bg_layer, mask)

        # Render sections to box layer
        section_layer = Image.new("RGBA", self.page.wh, (0,0,0,0))
        for section in self.__sections:
            render = self.__sections[section].render()
            pos = self.__sections[section].pos
            section_layer.paste(render, (pos.x + self.__pos.x, pos.y + self.__pos.y))
        page = Image.alpha_composite(page, section_layer)

        # # Render border layer
        # if 'border' in self.__data and 'color' in self.__data['border']:
        #     border_color = self.__data['border']['color']
        # else:
        #     border_color = "black"
        # if 'border' in self.__data and 'width' in self.__data['border']:
        #     border_width = int(self.__data['border']['width'])
        # else:
        #     border_width = 4

        border_color = 'black'
        border_width = 4
        border_layer = Image.new("RGBA", self.page.wh, (0,0,0,0))
        for section in self.__sections:
            border = self.__sections[section].render_border(border_color, border_width)
            pos = self.__sections[section].pos
            border_layer.alpha_composite(border, (pos.x + self.__pos.x - border_width, pos.y + self.__pos.y - border_width))

        # Cut out interior
        clear = Image.new("RGBA", self.page.wh, (0,0,0,0))
        border_layer = Image.composite(border_layer, clear, mask)
        page.alpha_composite(border_layer)

        # # Add on cut / guide lines.

        page.show()

    def test_generate(self):
        clear = (0,0,0,0)

        # Take a transparent image
        page = Image.new("RGBA", (500, 500), clear)
        # And a second transparent image, with a thing on it.
        box_layer = Image.new("RGBA", (500, 500), clear)
        box_layer_draw = ImageDraw.Draw(box_layer, "RGBA")
        box_layer_draw.rectangle((100, 100,400,400), fill="white")
        box_layer.show()
        # And make a mask that cuts off half of it
        mask = Image.new("L", (500, 500), "black")
        mask_draw = ImageDraw.Draw(mask, "L")
        mask_draw.rectangle((250,0,500,500), fill="white")
        mask.show()
        # Then do a composite, with the mask:
        final = Image.composite(page, box_layer, mask)
        final.show()


    def __repr__(self):
        attributes = []
        attributes.append(f"Box Settings:")
        attributes.append(f"Config:\n{self.__config}")
        attributes.append(f"Page: {self.__page}")
        attributes.append(f"Dim: {self.__dim}")
        attributes.append(f"Tabs: {self.__tabs}")
        attributes.append(f"Pos: {self.__pos}")
        attributes.append(f"Size: {self.__size}")
        attributes.append("")
        attributes.append(f"Sections:")
        for section in self.__sections:
            attributes.append(f"{section}")
            attributes.append(f"{self.__sections[section]}")
            attributes.append("")


        return "\n".join(attributes)