import pytest
from bgboxmaker import CommonConfig

class TestCommonConfig():
    """Test code for CommonConfig class."""

    @pytest.fixture()
    def config(self):
        config : CommonConfig = CommonConfig()
        yield config


    def test_repr(self, config : CommonConfig) -> None:
        print(config)


    def test_init_update(self) -> None:
        config : CommonConfig = CommonConfig({"margin" : 1})
        assert config.margin == 1


    def test_set_margin(self, config : CommonConfig) -> None:
        config.margin = 0.2
        assert config.margin == 0.2


    def test_update_data_font(self, config : CommonConfig) -> None:
        config.update_data({"font" : {"name" : "Garamond.ttf"}})
        assert config.font.name == "Garamond.ttf"


    def test_update_data_margin(self, config : CommonConfig) -> None:
        config.update_data({"margin" : 0.2})
        assert config.margin == 0.2


    def test_update_data_image_source(self, config : CommonConfig) -> None:
        config.update_data({"image_source" : "path"})
        assert config.image_source == "path"


    def test_update_data_resolution(self, config : CommonConfig) -> None:
        config.update_data({"resolution" : 200})
        assert config.resolution == 200
