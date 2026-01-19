import pytest
from unittest.mock import patch
from bgboxmaker.dim import Dim
from bgboxmaker.model import SectionConfig, FeatureConfig, CommonConfig, SectionType, Orientation, FeatureType
from bgboxmaker.view import Section, PanelFeature, TextFeature, ImageFeature
from PIL import Image, ImageDraw


class TestSection():
    """Test code for Section class."""

    @pytest.fixture()
    def section(self):
        common = CommonConfig()
        config : SectionConfig = SectionConfig(common)
        yield Section(config)

    @pytest.fixture()
    def test_image(self):
        yield Image.new("RGB", (100, 200), "white")


    def test_init_with_rotated(self) -> None:
        common = CommonConfig()
        data = {}
        data['rotated'] = True
        config : SectionConfig = SectionConfig(common, data)
        section = Section(config)
        assert section.rotated


    def test_init_with_landscape(self) -> None:
        common = CommonConfig()
        data = {}
        data['orientation'] = "landscape"
        config : SectionConfig = SectionConfig(common, data)
        section = Section(config)
        assert section.orientation == Orientation.LANDSCAPE


    def test_config(self, section : Section) -> None:
        common = CommonConfig()
        config : SectionConfig = SectionConfig(common)
        assert str(section.config) == str(config)


    def test_set_pos(self, section : Section) -> None:
        section.pos = Dim(40, 500)
        assert section.pos == Dim(40, 500)


    def test_set_size(self, section : Section) -> None:
        section.size = Dim(400, 700)
        assert section.size == Dim(400, 700)


    def test_set_rotated(self, section : Section) -> None:
        section.rotated = True
        assert section.rotated


    def test_set_flip_h(self, section : Section) -> None:
        section.flip_h = True
        assert section.flip_h


    def test_set_flip_v(self, section : Section) -> None:
        section.flip_v = True
        assert section.flip_v


    def test_set_type(self, section : Section) -> None:
        section.type = SectionType.BACK
        assert section.type == SectionType.BACK


    def test_set_cutin(self, section : Section) -> None:
        section.cutin = 200
        assert section.cutin == 200


    def test_set_orientation(self, section : Section) -> None:
        section.orientation = Orientation.LANDSCAPE
        assert section.orientation == Orientation.LANDSCAPE


    def test_set_print_orientation(self, section : Section) -> None:
        section.print_orientation = Orientation.LANDSCAPE
        assert section.print_orientation == Orientation.LANDSCAPE


    def test_fix_size(self, section : Section) -> None:
        section.size = Dim(40, 80)
        section.orientation = Orientation.LANDSCAPE
        assert section.size == Dim(80, 40)


    def test_fix_orientation_orientation(self, section : Section, test_image : Image.Image) -> None:
        """Test changing orientation"""
        section.orientation = Orientation.LANDSCAPE
        fixed = section._fix_orientation(test_image)
        assert fixed.size == (200, 100)


    def test_fix_orientation_rotated(self, section : Section, test_image : Image.Image) -> None:
        """Test changing rotation"""
        section.rotated = True
        fixed = section._fix_orientation(test_image)
        assert fixed.size == (100, 200)


    def test_fix_orientation_flip_v(self, section : Section, test_image : Image.Image) -> None:
        """Test changing vertical flip"""
        section.flip_v = True
        fixed = section._fix_orientation(test_image)
        assert fixed.size == (100, 200)


    def test_fix_orientation_flip_h(self, section : Section, test_image : Image.Image) -> None:
        """Test changing horizontal flip"""
        section.flip_h = True
        fixed = section._fix_orientation(test_image)
        assert fixed.size == (100, 200)


    def test_draw_shapes_pane(self, show_images : bool, section : Section) -> None:
        """Test _draw_shapes for pane / glue tab"""
        section.type = SectionType.PANE
        shape = section._draw_shapes("RGBA", Dim(200,200), "#00000000", "aqua")
        if show_images:
            draw = ImageDraw.Draw(shape)
            draw.text((0,180), text="Section._draw_shapes: Panel", fill="black")
            shape.show()
        assert shape.size == (200, 200)


    def test_draw_shapes_side_tab(self, show_images : bool, section : Section) -> None:
        """Test _draw_shapes for side tab"""
        section.type = SectionType.SIDE_TAB
        shape = section._draw_shapes("RGBA", Dim(200,200), "#00000000", "aqua")
        if show_images:
            draw = ImageDraw.Draw(shape)
            draw.text((0,180), text="Section._draw_shapes: Side Tab", fill="black")
            shape.show()
        assert shape.size == (200, 200)


    def test_draw_shapes_tuck_tab(self, show_images : bool, section : Section) -> None:
        """Test _draw_shapes for tuck tab"""
        section.type = SectionType.TUCK_TAB
        shape = section._draw_shapes("RGBA", Dim(200,200), "#00000000", "aqua")
        if show_images:
            draw = ImageDraw.Draw(shape)
            draw.text((0,100), text="Section._draw_shapes: Tuck Tab", fill="black")
            shape.show()
        assert shape.size == (200, 200)


    def test_draw_shapes_back(self, show_images : bool, section : Section) -> None:
        """Test _draw_shapes for back"""
        section.type = SectionType.BACK
        section.cutin = 100
        shape = section._draw_shapes("RGBA", Dim(200,200), "#00000000", "aqua")
        if show_images:
            draw = ImageDraw.Draw(shape)
            draw.text((0,180), text="Section._draw_shapes: Back", fill="black")
            shape.show()
        assert shape.size == (200, 200)


    def test_get_border(self, show_images : bool, section : Section) -> None:
        """Test _get_border"""
        section.size = Dim(200,200)
        section.type = SectionType.SIDE_TAB
        border = section._get_border("black", 5)
        if show_images:
            draw = ImageDraw.Draw(border)
            draw.text((10, 180), text="_get_border", fill="white")
            border.show()
        assert border.size == (210, 210)


    def test_get_mask(self, show_images : bool, section : Section) -> None:
        """Test _get_mask"""
        section.size = Dim(200,200)
        section.type = SectionType.SIDE_TAB
        border = section._get_mask()
        if show_images:
            draw = ImageDraw.Draw(border)
            draw.text((10, 180), text="_get_mask", fill="white")
            border.show()
        assert border.size == (200, 200)


    def test_get_margin(self, section : Section) -> None:
        """Test _get_margin normally"""
        section.config.common.margin = 0.25
        section.size = Dim(200, 200)
        margin = section._get_margin()
        assert isinstance(margin, int) and margin == 75


    def test_get_margin_squished(self, section : Section) -> None:
        """Test _get_margin with small size"""
        section.config.common.margin = 0.25
        section.size = Dim(100, 50)
        margin = section._get_margin()
        assert isinstance(margin, int) and margin == 20


    def test_get_hard_bounds(self, section : Section) -> None:
        """Test _get_hard_bounds"""
        section.size = Dim(100,200)
        bounds : Dim = section._get_hard_bounds(10)
        assert bounds.xy == (80, 180)


    def test_get_feature_bounds_w(self, section : Section) -> None:
        """Test _get_feature_bounds with width"""
        data : dict = {
            "type" : "image",
            "width" : 1,
            "options" : {"image" : "image.jpg"}
            }
        config : FeatureConfig = FeatureConfig(section.config.common, data)
        bounds = Dim(1000, 2000)
        feature_bounds = section._get_feature_bounds(config, bounds)
        assert feature_bounds.xy == (300, 2000)


    def test_get_feature_bounds_w_excess(self, section : Section) -> None:
        """Test _get_feature_bounds with width larger than bounds"""
        data : dict = {
            "type" : "image",
            "width" : 1,
            "options" : {"image" : "image.jpg"}
            }
        config : FeatureConfig = FeatureConfig(section.config.common, data)
        bounds = Dim(100, 200)
        feature_bounds = section._get_feature_bounds(config, bounds)
        assert feature_bounds.xy == (100, 200)


    def test_get_feature_bounds_h(self, section : Section) -> None:
        """Test _get_feature_bounds with height"""
        data : dict = {
            "type" : "image",
            "height" : 1,
            "options" : {"image" : "image.jpg"}
            }
        config : FeatureConfig = FeatureConfig(section.config.common, data)
        bounds = Dim(1000, 2000)
        feature_bounds = section._get_feature_bounds(config, bounds)
        assert feature_bounds.xy == (1000, 300)


    def test_get_feature_bounds_h_excess(self, section : Section) -> None:
        """Test _get_feature_bounds with height larger than bounds"""
        data : dict = {
            "type" : "image",
            "height" : 1,
            "options" : {"image" : "image.jpg"}
            }
        config : FeatureConfig = FeatureConfig(section.config.common, data)
        bounds = Dim(100, 200)
        feature_bounds = section._get_feature_bounds(config, bounds)
        assert feature_bounds.xy == (100, 200)


    def test_get_feature_bounds_wh(self, section : Section) -> None:
        """Test _get_feature_bounds with width and height"""
        data : dict = {
            "type" : "image",
            "height" : 1,
            "width" : 1,
            "options" : {"image" : "image.jpg"}
            }
        config : FeatureConfig = FeatureConfig(section.config.common, data)
        bounds = Dim(1000, 2000)
        feature_bounds = section._get_feature_bounds(config, bounds)
        assert feature_bounds.xy == (300, 300)


    def test_get_feature_bounds_wh_excess(self, section : Section) -> None:
        """Test _get_feature_bounds with width and height larger than bounds"""
        data : dict = {
            "type" : "image",
            "height" : 1,
            "width" : 1,
            "options" : {"image" : "image.jpg"}
            }
        config : FeatureConfig = FeatureConfig(section.config.common, data)
        bounds = Dim(100, 200)
        feature_bounds = section._get_feature_bounds(config, bounds)
        assert feature_bounds.xy == (100, 100)


    def test_get_feature_bounds_wh_excess2(self, section : Section) -> None:
        """Test _get_feature_bounds with width and height larger than bounds"""
        data : dict = {
            "type" : "image",
            "height" : 1,
            "width" : 1,
            "options" : {"image" : "image.jpg"}
            }
        config : FeatureConfig = FeatureConfig(section.config.common, data)
        bounds = Dim(200, 100)
        feature_bounds = section._get_feature_bounds(config, bounds)
        assert feature_bounds.xy == (100, 100)


    def test_get_features(self, show_images : bool, section : Section) -> None:
        data : dict = {}
        data['type'] = "text"
        data['options'] = {"text" : "text"}
        feature = FeatureConfig(section.config.common, data)
        section.size = Dim(600, 800)
        section.config.features.append(feature)
        feature_layer = section._get_features()
        if show_images:
            draw = ImageDraw.Draw(feature_layer)
            draw.text((0,180), text="Section._get_features", fill="black")
            feature_layer.show()
        assert isinstance(feature_layer, Image.Image)


    def test_feature_factory_panel(self, section : Section) -> None:
        data = {"type" : "panel", "width" : 2, "height" : 2}
        config = FeatureConfig(section.config.common, data)
        feature = section._feature_factory(config)
        assert isinstance(feature, PanelFeature)


    def test_feature_factory_text(self, section : Section) -> None:
        data = {"type" : "text", "options" : {"text" : "text"}}
        config = FeatureConfig(section.config.common, data)
        feature = section._feature_factory(config)
        assert isinstance(feature, TextFeature)


    def test_feature_factory_image(self, section : Section) -> None:
        data = {"type" : "image", "options" : {"image" : "image.jpg"}}
        config = FeatureConfig(section.config.common, data)
        feature = section._feature_factory(config)
        assert isinstance(feature, ImageFeature)


    def test_render_wo_features(self, show_images : bool, section : Section) -> None:
        section.size = Dim(200, 300)
        render = section.render()
        if show_images:
            draw = ImageDraw.Draw(render)
            draw.text((0,180), text="Section._render: No features", fill="black")
            render.show()
        assert render.size == (200, 300)


    def test_render_w_features(self, show_images : bool, section : Section) -> None:
        section.size = Dim(200, 300)
        data = {"type" : "text", "options" : {"text" : "text"}}
        config = FeatureConfig(section.config.common, data)
        section.config.features.append(config)
        render = section.render()
        if show_images:
            draw = ImageDraw.Draw(render)
            draw.text((0,180), text="Section._render: No features", fill="black")
            render.show()
        assert render.size == (200, 300)


    def test_render_mask(self, show_images : bool, section : Section) -> None:
        section.size = Dim(200, 300)
        render = section.render_mask()
        if show_images:
            draw = ImageDraw.Draw(render)
            draw.text((0,180), text="Section._render_mask", fill="white")
            render.show()
        assert render.size == (200, 300)


    def test_render_border(self, show_images : bool, section : Section) -> None:
        section.size = Dim(200, 300)
        render = section.render_border("black", 10)
        if show_images:
            draw = ImageDraw.Draw(render)
            draw.text((0,180), text="Section._render_border", fill="white")
            render.show()
        assert render.size == (220, 320)


    def test_repr(self, section : Section) -> None:
        print(section)

