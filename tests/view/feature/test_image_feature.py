import pytest
from unittest.mock import patch
from bgboxmaker.dim import Dim
from bgboxmaker.model import FeatureConfig, CommonConfig
from bgboxmaker.view.feature import ImageFeature
from PIL import Image


class TestImageFeature():
    """Test code for ImageFeature class."""

    @pytest.fixture()
    def feature(self):
        common = CommonConfig()
        data = {}
        data['type'] = "image"
        data['options'] = {}
        data['options']['image'] = "image.png"
        config = FeatureConfig(common, data)
        yield ImageFeature(config)



    def test_get_image(self, feature : ImageFeature) -> None:
        image = feature._get_image('./test_image.png')
        assert isinstance(image, Image.Image)


    def test_get_image_fail(self, feature : ImageFeature) -> None:
        with pytest.raises(FileNotFoundError):
            image = feature._get_image('./missingimage.png')


    def test_render_new_aspect(self) -> None:
        with patch.object(ImageFeature, '_get_image') as mock_image:
            mock_image.return_value = Image.new("RGBA", (100,400), "black")
            common = CommonConfig()
            data = {}
            data['type'] = "image"
            data['width'] = 400
            data['height'] = 500
            data['options'] = {}
            data['options']['image'] = "image.png"
            config = FeatureConfig(common, data)
            feature = ImageFeature(config)

            render = feature.render(Dim(800, 800))
            assert render.size == (800, 800)


    def test_render_upscale_height(self, feature : ImageFeature):
        with patch.object(ImageFeature, '_get_image') as mock_image:
            mock_image.return_value = Image.new("RGBA", (100,400), "black")
            render = feature.render(Dim(800, 800))
            assert render.size == (200, 800)


    def test_render_upscale_width(self, feature : ImageFeature):
        with patch.object(ImageFeature, '_get_image') as mock_image:
            mock_image.return_value = Image.new("RGBA", (400,100), "black")
            render = feature.render(Dim(800, 800))
            assert render.size == (800, 200)


    def test_render_downscale_height(self, feature : ImageFeature):
        with patch.object(ImageFeature, '_get_image') as mock_image:
            mock_image.return_value = Image.new("RGBA", (800,800), "black")
            render = feature.render(Dim(100, 400))
            assert render.size == (100, 100)


    def test_render_downscale_width(self, feature : ImageFeature):
        with patch.object(ImageFeature, '_get_image') as mock_image:
            mock_image.return_value = Image.new("RGBA", (800,800), "black")
            render = feature.render(Dim(400, 100))
            assert render.size == (100, 100)
