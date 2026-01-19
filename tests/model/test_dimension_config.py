import pytest
from bgboxmaker import DimensionConfig, ConfigurationError

class TestDimensionConfig():
    """Test code for DimensionConfig class."""

    @pytest.fixture()
    def config(self):
        data : dict = {"width" : 2.5, "height" : 3.5, "depth" : 1}
        config : DimensionConfig = DimensionConfig(data)
        yield config


    def test_repr(self, config : DimensionConfig) -> None:
        print(config)


    def test_update_data_width_true(self, config : DimensionConfig) -> None:
        assert config.width == 2.5


    def test_update_data_height_true(self, config : DimensionConfig) -> None:
        assert config.height == 3.5


    def test_update_data_depth_true(self, config : DimensionConfig) -> None:
        assert config.depth == 1


    def test_update_data_width_false(self) -> None:
        with pytest.raises(ConfigurationError):
            config = DimensionConfig({"height" : 3.5, "depth" : 1})


    def test_update_data_height_false(self) -> None:
        with pytest.raises(ConfigurationError):
            config = DimensionConfig({"width" : 2.5, "depth" : 1})


    def test_update_data_depth_false(self) -> None:
        with pytest.raises(ConfigurationError):
            config = DimensionConfig({"width" : 2.5, "height" : 3.5})
