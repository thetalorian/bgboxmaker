import pytest
from bgboxmaker import BasicConfig, ConfigurationError

class TestBasicConfig():
    """Test code for BasicConfig class."""

    @pytest.fixture()
    def config(self):
        data : dict = {"title" : "title", "subtitle" : "subtitle", "extra" : "1"}
        config : BasicConfig = BasicConfig(data)
        yield config


    def test_repr(self, config : BasicConfig) -> None:
        print(config)


    def test_update_data_title(self, config : BasicConfig) -> None:
        assert config.title == "title"


    def test_update_data_subtitle(self, config : BasicConfig) -> None:
        assert config.subtitle == "subtitle"


    def test_update_data_extra(self, config : BasicConfig) -> None:
        assert config.extra == "1"

