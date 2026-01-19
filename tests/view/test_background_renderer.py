import pytest
from unittest.mock import patch
from bgboxmaker.dim import Dim
from bgboxmaker.model import BackgroundConfig, CommonConfig
from bgboxmaker.view import BackgroundRenderer
from PIL import Image, ImageDraw


class TestBackgroundRenderer():
    """Test code for BackgroundRenderer class."""

    @pytest.fixture()
    def renderer(self):
        common = CommonConfig()
        data = {}
        data['image'] = "image.png"
        data['color'] = "gray"
        config = BackgroundConfig(common, data)
        yield BackgroundRenderer(config)


    def test_render_color(self, show_images : bool) -> None:
        common : CommonConfig = CommonConfig()
        data : dict = {"color" : "green"}
        config : BackgroundConfig = BackgroundConfig(common, data)
        renderer = BackgroundRenderer(config)
        render = renderer.render(Dim(500, 400))
        if show_images:
            draw = ImageDraw.Draw(render)
            draw.text((0,0), text="BackgroundRenderer: Color", fill="black")
            render.show()
        assert isinstance(render, Image.Image) and render.size == (500, 400)


    def test_get_image(self, renderer : BackgroundRenderer) -> None:
        image = renderer._get_image('./test_image.png')
        assert isinstance(image, Image.Image)


    def test_get_image_fail(self, renderer : BackgroundRenderer) -> None:
        with pytest.raises(FileNotFoundError):
            image = renderer._get_image('./missingimage.png')


    def test_render_too_wide(self, renderer : BackgroundRenderer):
        with patch.object(BackgroundRenderer, '_get_image') as mock_image:
            mock_image.return_value = Image.new("RGBA", (800,500), "gray")
            render = renderer.render(Dim(400, 400))
            assert render.size == (400, 400)


    def test_render_too_tall(self, renderer : BackgroundRenderer):
        with patch.object(BackgroundRenderer, '_get_image') as mock_image:
            mock_image.return_value = Image.new("RGBA", (500,800), "gray")
            render = renderer.render(Dim(400, 400))
            assert render.size == (400, 400)


    def test_render_too_small(self, renderer : BackgroundRenderer):
        with patch.object(BackgroundRenderer, '_get_image') as mock_image:
            mock_image.return_value = Image.new("RGBA", (50,80), "gray")
            render = renderer.render(Dim(400, 400))
            assert render.size == (400, 400)
