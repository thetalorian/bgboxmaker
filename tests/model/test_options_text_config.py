import pytest
from bgboxmaker import OptionsTextConfig, CommonConfig, ConfigurationError

class TestOptionsTextConfig():
    """Test code for OptionsTextConfig class."""

    @pytest.fixture()
    def config(self):
        common : CommonConfig = CommonConfig()
        config : OptionsTextConfig = OptionsTextConfig(common)
        yield config


    def test_init_update(self) -> None:
        common : CommonConfig = CommonConfig()
        config : OptionsTextConfig = OptionsTextConfig(common, {"text" : "hello"})
        assert config.text == "hello"


    def test_set_text(self, config : OptionsTextConfig) -> None:
        config.text = "goodbye"
        assert config.text == "goodbye"


    def test_set_align(self, config : OptionsTextConfig) -> None:
        config.align = "right"
        assert config.align == "right"


    def test_valid_multiline_true(self, config : OptionsTextConfig) -> None:
        assert config._valid_multiline(["line 1", "line 2"])


    def test_valid_multiline_false(self, config : OptionsTextConfig) -> None:
        assert not config._valid_multiline(["line 1", 2])


    def test_valid_align_true(self, config : OptionsTextConfig) -> None:
        assert config._valid_align("left")


    def test_valid_align_false(self, config : OptionsTextConfig) -> None:
        assert not config._valid_align("apple")


    def test_update_data_text_str(self, config : OptionsTextConfig) -> None:
        config.update_data({"text" : "text"})
        assert config.text == "text"


    def test_update_data_text_lines(self, config : OptionsTextConfig) -> None:
        config.update_data({"text" : ["line 1", "line 2"]})
        assert config.text == "line 1\nline 2"


    def test_update_data_text_missing(self, config : OptionsTextConfig) -> None:
        with pytest.raises(ConfigurationError):
            config.update_data({"align" : "left"})


    def test_update_data_align(self, config : OptionsTextConfig) -> None:
        config.update_data({"text" : "hello", "align" : "right"})
        assert config.align == "right"


    def test_update_data_font(self, config : OptionsTextConfig) -> None:
        config.update_data({"text" : "hello", "font" : {"size" : 20}})
        assert config.common.font.size == 20


    def test_repr(self, config : OptionsTextConfig) -> None:
        print(config)
