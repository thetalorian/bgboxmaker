import pytest
from unittest.mock import patch
from bgboxmaker.dim import Dim
from bgboxmaker.model import FeatureConfig, CommonConfig
from bgboxmaker.view.feature import PanelFeature
from PIL import Image, ImageDraw


class TestPanelFeature():
    """Test code for ImageFeature class."""


    def test_render_panel_no_border(self, show_images) -> None:
        common = CommonConfig()
        data = {}
        data['type'] = "panel"
        data['options'] = {}
        data['options']['color'] = "aqua"
        config = FeatureConfig(common, data)
        panel_feature = PanelFeature(config)
        panel = panel_feature.render(Dim(200,100))
        if show_images:
            draw = ImageDraw.Draw(panel)
            draw.text((0,0), text="Panel Feature Borderless", fill="black")
            panel.show()
        assert isinstance(panel, Image.Image)

    def test_render_panel_border(self, show_images) -> None:
        common = CommonConfig()
        data = {}
        data['type'] = "panel"
        data['options'] = {}
        data['options']['color'] = "aqua"
        data['options']['border'] = "green"
        data['options']['border_width'] = 10
        config = FeatureConfig(common, data)
        panel_feature = PanelFeature(config)
        panel = panel_feature.render(Dim(200,100))
        if show_images:
            draw = ImageDraw.Draw(panel)
            draw.text((0,0), text="Panel Feature Bordered", fill="black")
            panel.show()
        assert isinstance(panel, Image.Image)

