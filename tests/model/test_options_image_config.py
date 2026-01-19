import pytest
from bgboxmaker import OptionsImageConfig, CommonConfig, ConfigurationError

class TestOptionsImageConfig():
    """Test code for OptionsImageConfig class."""

    @pytest.fixture()
    def config(self):
        common : CommonConfig = CommonConfig()
        config : OptionsImageConfig = OptionsImageConfig(common, {"image" : "image.jpg"})
        yield config


    def test_init_update(self) -> None:
        common : CommonConfig = CommonConfig()
        config : OptionsImageConfig = OptionsImageConfig(common, {"image" : "image.jpg"})
        assert config.image == "image.jpg"


    def test_update_data_image(self, config : OptionsImageConfig) -> None:
        config.update_data({"image" : "image2.jpg"})
        assert config.image == "image2.jpg"


    def test_update_data_image_missing(self, config : OptionsImageConfig) -> None:
        with pytest.raises(ConfigurationError):
            config.update_data({})


    def test_update_data_image_config(self, config : OptionsImageConfig) -> None:
        config.update_data({"image" : "image.jpg", "image_source" : "path"})
        assert config.common.image_source == "path"


    def test_repr(self, config : OptionsImageConfig) -> None:
        print(config)
