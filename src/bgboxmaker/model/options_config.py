from abc import ABC, abstractmethod
from bgboxmaker.model import Config, CommonConfig
import logging
logger = logging.getLogger(__name__)

class OptionsConfig(Config):
    """Abstract class for feature options."""

    @abstractmethod
    def __init__(self, common : CommonConfig, data : dict): # pragma: no cover
        pass
