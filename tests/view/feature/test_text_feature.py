import pytest
from unittest.mock import patch
from bgboxmaker.dim import Dim
from bgboxmaker.model import FeatureConfig, CommonConfig
from bgboxmaker.view.feature import TextFeature
from PIL import Image, ImageDraw


class TestTextFeature():
    """Test code for TextFeature class."""

    @pytest.fixture()
    def feature(self):
        common = CommonConfig()
        data = {}
        data['type'] = "text"
        data['options'] = {}
        data['options']['text'] = "hello world"
        config = FeatureConfig(common, data)
        yield TextFeature(config)


    def test_render_just_right(self, show_images : bool, feature : TextFeature) -> None:
        render = feature.render(Dim(800,100))
        if show_images:
            draw = ImageDraw.Draw(render)
            draw.text((0,50), text="ImageFeature", fill="black")
            render.show()
        assert render.size == (800, 100)


    def test_render_too_big(self, show_images : bool, feature : TextFeature) -> None:
        render = feature.render(Dim(80,100))
        if show_images:
            draw = ImageDraw.Draw(render)
            draw.text((0,50), text="ImageFeature:too_big", fill="black")
            render.show()
        assert render.size == (80, 100)
