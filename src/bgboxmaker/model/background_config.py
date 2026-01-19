from bgboxmaker.model import Config, CommonConfig

class BackgroundConfig(Config):
    """Holds background configuration."""

    def __init__(self, common : CommonConfig, data : dict = {}):
        self.__keys = ['color', 'image', 'image_source']
        self.__common = common
        self.__color : str = ""
        self.__image : str = ""
        if data:
            self.update_data(data)

    @property
    def common(self) -> CommonConfig:
        return self.__common

    @property
    def color(self) -> str:
        return self.__color

    @property
    def image(self) -> str:
        return self.__image

    @property
    def image_path(self) -> str:
        return f"{self.common.image_source}/{self.image}"

    @property
    def isSet(self) -> bool:
        return self.__image != "" or self.__color != ""

    def update_data(self, data):
        """Process given data."""

        self._validate_keys(data, "'background' block", self.__keys)

        if 'color' in data:
            self.__color = self._validate(data['color'], 'background color', [self._valid_str])

        if 'image' in data:
            self.__image = self._validate(data['image'], 'background image', [self._valid_str])

        if 'image_source' in data:
            self.common.image_source = self._validate(data['image_source'], 'image source', [self._valid_str])


    def __repr__(self) -> str:
        attributes : list[str] = []
        attributes.append(f"Common: {self.__common}")
        attributes.append(f"Color: {self.__color}")
        attributes.append(f"Image: {self.__image}")
        return "{" + ", ".join(attributes) + "}"
