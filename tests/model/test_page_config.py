import pytest
from bgboxmaker import PageConfig

class TestPageConfig():
    """Test code for PageConfig class"""

    @pytest.fixture()
    def config(self):
        config : PageConfig = PageConfig({})
        yield config


    def test_repr(self, config : PageConfig) -> None:
        print(config)


    def test_update_data_width(self, config : PageConfig) -> None:
        config.update_data({"width" : 20})
        assert config.width == 20


    def test_update_data_height(self, config : PageConfig) -> None:
        config.update_data({"height" : 2})
        assert config.height == 2


    def test_update_data_margin(self, config : PageConfig) -> None:
        config.update_data({"margin" : 2})
        assert config.margin == 2


    def test_update_data_thickness(self, config : PageConfig) -> None:
        config.update_data({"thickness" : 2})
        assert config.thickness == 2


    def test_check_orientation(self, config : PageConfig) -> None:
        config.update_data({"width" : 2, "height" : 3})
        assert config.width == 3 and config.height == 2






