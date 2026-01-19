import pytest
from bgboxmaker import OptionsPanelConfig, CommonConfig, ConfigurationError

class TestOptionsPanelConfig():
    """Test code for OptionsPanelConfig class."""

    @pytest.fixture()
    def config(self):
        common : CommonConfig = CommonConfig()
        config : OptionsPanelConfig = OptionsPanelConfig(common, {})
        yield config


    def test_init_update(self) -> None:
        common : CommonConfig = CommonConfig()
        config : OptionsPanelConfig = OptionsPanelConfig(common, {"color" : "red"})
        assert config.color == "red"


    def test_update_data_color(self, config : OptionsPanelConfig) -> None:
        config.update_data({"color" : "red"})
        assert config.color == "red"


    def test_update_data_border(self, config : OptionsPanelConfig) -> None:
        config.update_data({"border" : "red"})
        assert config.border == "red"


    def test_update_data_border_width(self, config : OptionsPanelConfig) -> None:
        config.update_data({"border_width" : 7})
        assert config.border_width == 7


    def test_repr(self, config : OptionsPanelConfig) -> None:
        print(config)
