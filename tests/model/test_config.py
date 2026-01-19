import pytest
from bgboxmaker import Config, BasicConfig, ConfigurationError, SectionName

class TestConfig():
    """Test code for Config class."""

    @pytest.fixture()
    def config(self):
        config : Config = BasicConfig()
        yield config


    def test_log_block(self, config : Config) -> None:
        config._log_block("message")


    def test_found(self, config : Config) -> None:
        config._found("message")


    def test_missing_required(self, config : Config) -> None:
        with pytest.raises(ConfigurationError):
            config._missing_required("message")


    def test_validate_keys_true(self, config : Config) -> None:
        config._validate_keys({"a": 1, "b" : 2}, "test", ["a", "b"])


    def test_validate_keys_false(self, config : Config) -> None:
        with pytest.raises(ConfigurationError):
            config._validate_keys({"a": 1, "b" : 2, "c": 3}, "test", ["a", "b"])


    def test_validate_enum_true(self, config : Config) -> None:
        config._validate_enum("front", "test", SectionName)


    def test_validate_enum_false(self, config : Config) -> None:
        with pytest.raises(ConfigurationError):
            config._validate_enum("warble", "test", SectionName)


    def test_validate_true(self, config : Config) -> None:
        assert config._validate(1, "input", [config._valid_int])


    def test_validate_false(self, config : Config) -> None:
        with pytest.raises(ConfigurationError):
            config._validate("hamburger", "input", [config._valid_int])


    def test_valid_str_true(self, config : Config) -> None:
        assert config._valid_str("hamburger")


    def test_valid_str_false(self, config : Config) -> None:
        assert not config._valid_str(8)


    def test_valid_bool_true(self, config : Config) -> None:
        assert config._valid_bool(True)


    def test_valid_bool_false(self, config : Config) -> None:
        assert not config._valid_bool(8)


    def test_valid_int_true(self, config : Config) -> None:
        assert config._valid_int(1)


    def test_valid_int_false(self, config : Config) -> None:
        assert not config._valid_int("hamburger")


    def test_valid_num_int(self, config : Config) -> None:
        assert config._valid_num(1)


    def test_valid_num_float(self, config : Config) -> None:
        assert config._valid_num(2.5)


    def test_valid_num_str(self, config : Config) -> None:
        assert not config._valid_num("hamburger")


    def test_valid_gt_zero_true(self, config : Config) -> None:
        assert config._valid_gt_zero(1)


    def test_valid_gt_zero_false(self, config : Config) -> None:
        assert not config._valid_gt_zero(0)


    def test_valid_gte_zero_true(self, config : Config) -> None:
        assert config._valid_gte_zero(0)


    def test_valid_gte_zero_false(self, config : Config) -> None:
        assert not config._valid_gte_zero(-2)


    def test_valid_list_true(self, config : Config) -> None:
        assert config._valid_list([2, 1])


    def test_valid_list_false(self, config : Config) -> None:
        assert not config._valid_list(8) and not config._valid_list("hamburger")


    def test_valid_Vec2_int_true(self, config : Config) -> None:
        assert config._valid_Vec2_int([1, 2])


    def test_valid_Vec2_int_false(self, config : Config) -> None:
        assert not config._valid_Vec2_int([1, 1.5]) and not config._valid_Vec2_int([1, 2, 3])


    def test_valid_Vec2_gt_zero_true(self, config : Config) -> None:
        assert config._valid_Vec2_gt_zero([1, 2])


    def test_valid_Vec2_gt_zero_false(self, config : Config) -> None:
        assert not config._valid_Vec2_gt_zero([0,1])
