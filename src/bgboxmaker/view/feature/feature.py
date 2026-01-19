from abc import ABC, abstractmethod
from bgboxmaker import FeatureConfig, FeatureType
from PIL import Image
class Feature(ABC):
    """Abstract feature class

    Represents various visual element
    features that can be placed on the
    box by user configuration.
    """

    def __init__(self): # pragma: no cover
        pass


    @abstractmethod
    def render() -> Image.Image: # pragma: no cover
        pass