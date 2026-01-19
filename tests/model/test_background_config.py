import pytest
from bgboxmaker import BackgroundConfig, CommonConfig

class TestBackgroundConfig():
    """Test code for BackgroundConfig class."""

    @pytest.fixture()
    def config(self):
        common : CommonConfig = CommonConfig()
        config : BackgroundConfig = BackgroundConfig(common, {})
        yield config


    def test_init_update(self) -> None:
        common : CommonConfig = CommonConfig()
        config : BackgroundConfig = BackgroundConfig(common, {"color" : "red"})
        assert config.color == "red"


    def test_isSet_color(self, config : BackgroundConfig) -> None:
        config.update_data({"color" : "red"})
        assert config.isSet


    def test_isSet_image(self, config : BackgroundConfig) -> None:
        config.update_data({"image" : "image.jpg"})
        assert config.isSet


    def test_isSet_none(self, config : BackgroundConfig) -> None:
        assert not config.isSet


    def test_update_data_color(self, config : BackgroundConfig) -> None:
        config.update_data({"color": "red"})
        assert config.color == "red"


    def test_update_data_image(self, config : BackgroundConfig) -> None:
        config.update_data({"image" : "image.jpg"})
        assert config.image == "image.jpg"


    def test_update_data_image_source(self, config : BackgroundConfig) -> None:
        config.update_data({"image_source" : "./my/path"})
        assert config.common.image_source == "./my/path"


    def test_image_path(self, config : BackgroundConfig) -> None:
        assert config.image_path == "./"


    def test_repr(self, config : BackgroundConfig) -> None:
        print(config)
