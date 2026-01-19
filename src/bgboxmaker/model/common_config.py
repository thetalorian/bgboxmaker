from bgboxmaker.model import Config, FontConfig
import logging
logger = logging.getLogger(__name__)

class CommonConfig(Config):
    """Holds common configuration settings.

    Common configuration is passed down to sub-configurations
    as needed, and overridden when new values are supplied for
    those sub-configurations. Only one instance is instantiated,
    and gets copied and updated as required.

    Attributes
    ----------
    font : FontConfig
        Holds common font configuration settings. Can be
        overridden in DetailConfig or in OptionsTextConfig
        for text features.
    margin : float
        Margin provided in page units, used on all box
        sections. Can be overridden in DetailConfig
    image_source: str
        Common path to images. Can be overridden in
        DetailConfig or in OptionsImageConfig for
        image features.

    Methods
    -------
    update_data(data : dict) -> None:
        Takes a data block containing any of 'font', 'margin', or 'image_source'.
        Validates data and updates configuration as required.
    """

    def __init__(self, data = {}):
        """Initialize instance with default values."""
        self.__keys = ['font', 'margin', 'image_source', 'resolution']
        self.__font : FontConfig = FontConfig()
        self.__margin : float = 0.1
        self.__image_source : str = "."
        self.__resolution : int = 300
        if data:
            self.update_data(data)


    @property
    def font(self) -> FontConfig:
        return self.__font

    @property
    def margin(self) -> float:
        return self.__margin

    @margin.setter
    def margin(self, value : float) -> None:
        self.__margin = value

    @property
    def image_source(self) -> str:
        return self.__image_source

    @image_source.setter
    def image_source(self, value : str) -> None:
        self.__image_source = value

    @property
    def resolution(self) -> int:
        return self.__resolution

    def update_data(self, data : dict):
        """Process given data and update configuration as required."""

        self._validate_keys(data, "'common' block", self.__keys)

        if 'font' in data:
            self.font.update_data(data['font'])

        if 'margin' in data:
            self.__margin = self._validate(data['margin'], 'margin', [self._valid_num, self._valid_gt_zero])

        if 'image_source' in data:
            self.__image_source = self._validate(data['image_source'], 'image source', [self._valid_str])

        if 'resolution' in data:
            self.__resolution = self._validate(data['resolution'], 'resolution', [self._valid_int, self._valid_gt_zero])

    def __repr__(self) -> str:
        attributes : list[str] = []
        attributes.append(f"Font: {self.__font}")
        attributes.append(f"Margin: {self.__margin}")
        attributes.append(f"Image Source: {self.__image_source}")
        attributes.append(f"Resolution: {self.__resolution}")
        return "{" + ", ".join(attributes) + "}"