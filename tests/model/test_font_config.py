import pytest
from bgboxmaker import FontConfig

class TestFontConfig():
    """Test code for FontConfig class."""

    @pytest.fixture()
    def config(self):
        config : FontConfig = FontConfig()
        yield config


    def test_init_update(self) -> None:
        config : FontConfig = FontConfig({"name" : "Garamond.ttf"})
        assert config.name == "Garamond.ttf"


    def test_set_size(self, config : FontConfig) -> None:
        config.size = 50
        assert config.size == 50


    def test_valid_ttf_true(self, config : FontConfig) -> None:
        assert config._valid_ttf("Garamond.ttf")


    def test_valid_ttf_false(self, config : FontConfig) -> None:
        assert not config._valid_ttf("Garamond")


    def test_update_data_name(self, config : FontConfig) -> None:
        config.update_data({"name" : "Garamond.ttf"})
        assert config.name == "Garamond.ttf"


    def test_update_data_size(self, config : FontConfig) -> None:
        config.update_data({"size" : 20})
        assert config.size == 20


    def test_update_data_color(self, config : FontConfig) -> None:
        config.update_data({"color" : "red"})
        assert config.color == "red"


    def test_update_data_stroke(self, config : FontConfig) -> None:
        config.update_data({"stroke" : "red"})
        assert config.stroke == "red"


    def test_update_data_width(self, config : FontConfig) -> None:
        config.update_data({"width" : 6})
        assert config.width == 6


    def test_repr(self, config : FontConfig) -> None:
        print(config)
