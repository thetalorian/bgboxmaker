import pytest
from bgboxmaker import SectionConfig, CommonConfig, Orientation, Dim, FeatureConfig

class TestSectionConfig():
    """Test code for SectionConfig class"""

    @pytest.fixture()
    def config(self):
        common : CommonConfig = CommonConfig()
        config : SectionConfig = SectionConfig(common, {})
        yield config


    def test_repr(self, config : SectionConfig) -> None:
        feature_data = {"type" : "text", "options" : {"text" : "text"}}
        config.update_data({"features" : [feature_data]})
        print(config)


    def test_init_update(self) -> None:
        common : CommonConfig = CommonConfig()
        config : SectionConfig = SectionConfig(common, {"rotated" : True})
        assert config.rotated and config.rotated_is_set


    def test_set_grid(self, config : SectionConfig) -> None:
        config.grid = Dim(5, 5)
        assert config.grid == Dim(5, 5)


    def test_update_data_background(self, config : SectionConfig) -> None:
        config.update_data({"background" : {"color" : "red"}})
        assert config.background.color == "red"


    def test_update_data_rotated(self, config : SectionConfig) -> None:
        config.update_data({"rotated" : True})
        assert config.rotated and config.rotated_is_set


    def test_update_data_orientation(self, config : SectionConfig) -> None:
        config.update_data({"orientation" : "portrait"})
        assert config.orientation == Orientation.PORTRAIT and config.orientation_is_set


    def test_update_data_margin(self, config : SectionConfig) -> None:
        config.update_data({"margin" : 2})
        assert config.common.margin == 2


    def test_update_data_grid(self, config : SectionConfig) -> None:
        config.update_data({"grid" : [5, 5]})
        assert config.grid == Dim(5, 5)


    def test_update_data_features(self, config : SectionConfig) -> None:
        feature_data = {"type" : "text", "options" : {"text" : "text"}}
        config.update_data({"features" : [feature_data]})
        assert len(config.features) == 1 and str(config.features[0]) == str(FeatureConfig(config.common, feature_data))
