import pytest
from bgboxmaker import FeatureConfig, CommonConfig, FeatureType, Dim, OptionsTextConfig, ConfigurationError

class TestFeatureConfig():
    """Test code for FeatureConfig class"""

    @pytest.fixture()
    def config(self):
        common : CommonConfig = CommonConfig()
        config : FeatureConfig = FeatureConfig(common, {"type" : "text"})
        yield config


    def test_repr(self, config : FeatureConfig) -> None:
        print(config)


    def test_update_data_type(self, config : FeatureConfig) -> None:
        config.update_data({"type" : "panel"})
        assert config.type == FeatureType.PANEL

    def test_update_data_no_type(self, config : FeatureConfig) -> None:
        with pytest.raises(ConfigurationError):
            config.update_data({})


    def test_update_data_options(self, config : FeatureConfig) -> None:
        option_data = {"text" : "hello"}
        config.update_data({"type" : "text", "options" : option_data})
        options = OptionsTextConfig(config.common, option_data)
        assert str(config.options) == str(options)


    def test_update_data_width(self, config : FeatureConfig) -> None:
        config.update_data({"type" : "text", "width" : 1})
        assert config.width == 1


    def test_update_data_height(self, config : FeatureConfig) -> None:
        config.update_data({"type" : "text", "height" : 1})
        assert config.height == 1


    def test_update_data_place(self, config : FeatureConfig) -> None:
        config.update_data({"type" : "text", "place" : [1, 1]})
        assert config.place == Dim(1, 1)


    def test_update_data_anchor(self, config : FeatureConfig) -> None:
        config.update_data({"type" : "text", "anchor" : [1, 1]})
        assert config.anchor == Dim(1, 1)


    def test_set_type(self, config : FeatureConfig) -> None:
        config.type = FeatureType.PANEL
        assert config.type == FeatureType.PANEL


    def test_set_options(self, config : FeatureConfig) -> None:
        options = OptionsTextConfig(config.common, {"text" : "hello"})
        config.options = options
        assert str(config.options) == str(options)


    def test_set_place(self, config : FeatureConfig) -> None:
        config.place = Dim(2, 2)
        assert config.place == Dim(2, 2)


    def test_set_anchor(self, config : FeatureConfig) -> None:
        config.anchor = Dim(2, 2)
        assert config.anchor == Dim(2, 2)
