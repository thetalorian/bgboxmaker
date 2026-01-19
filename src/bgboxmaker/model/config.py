from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable, Union, TypeVar
from bgboxmaker.model import ConfigurationError
import logging
logger = logging.getLogger(__name__)
E = TypeVar('E', bound=Enum)


class Config(ABC):
    """Abstract configuration class

    Common configuration is passed down to sub-configurations
    as needed, and overridden when new values are supplied for
    those sub-configurations. Only one instance is instantiated,
    and gets copied and updated as required.

    Attributes
    ----------
    desc : str
        Description of class config block for use in logs.
    keys : list[str]
        List of allowed keys in input data dict.

    Methods
    -------
    _validate_keys(data : dict) -> None:
        Validates that all keys in provided data are in the allowed list of keys.
    """


    @abstractmethod
    def __init__(self, data : dict = {}): # pragma: no cover
        """Initialize instance with default values."""
        pass

    def _log_block(self, settings : str) -> None:
        """Log block settings."""
        logger.info(settings)

    def _found(self, config : str) -> None:
        """Logs finding of a config block."""
        logger.info(f"Block {config} found in configuration file.")


    def _missing_required(self, config : str) -> None:
        """Log and raise error for missing required parameters."""
        message = f"Required config {config} not provided."
        logger.error(message)
        raise ConfigurationError(message)


    def _validate_keys(self, data : dict, desc : str, keys : list[str]) -> None:
        """Validate input keys are allowed."""
        for key in data:
            if key not in keys:
                msg = f"Unknown configuration '{key}' found in {desc}."
                logger.error(msg)
                raise ConfigurationError(msg)

    def _validate_enum(self, input : str, desc : str, enum : type[E]) -> E:
        try:
            value = enum[input.upper()]
        except KeyError:
            msg = f"Unknown {desc} provided: {input}"
            logger.error(msg)
            raise ConfigurationError(msg)
        return value


    def _validate(self, input : Any, desc : str, validations : list[Callable]) -> Any:
        """Ensure all provided validations apply to input"""
        for validation in validations:
            if not validation(input):
                msg = f"Invalid {desc} provided: {input}"
                logger.error(msg)
                raise ConfigurationError(msg)

        logger.info(f"Setting {desc} to: {input}")
        return input


    def _valid_str(self, input : Any) -> bool:
        return isinstance(input, str)


    def _valid_bool(self, input : Any) -> bool:
        return isinstance(input, bool)


    def _valid_int(self, input: Any) -> bool:
        return isinstance(input, int)


    def _valid_num(self, input : Any) -> bool:
        return isinstance(input, (int, float))


    def _valid_gt_zero(self, input : Union[int, float]) -> bool:
        return input > 0


    def _valid_gte_zero(self, input : Union[int, float]) -> bool:
        return input >= 0


    def _valid_list(self, input : Any) -> bool:
        return isinstance(input, list)


    def _valid_Vec2_int(self, input : list) -> bool:
        return len(input) == 2 and isinstance(input[0], int) and isinstance(input[1], int)

    def _valid_Vec2_gt_zero(self, input : list) -> bool:
        return input[0] > 0 and input[1] > 0
