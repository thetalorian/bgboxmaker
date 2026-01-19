from bgboxmaker.model import CommonConfig, OptionsConfig

class OptionsImageConfig(OptionsConfig):
    """Holds options for an Image Feature."""

    def __init__(self, common : CommonConfig, data : dict = {}):
        self.__keys : list[str] = ['image', 'image_source']
        self.__common : CommonConfig = common
        self.__image : str
        if data:
            self.update_data(data)

    @property
    def common(self) -> CommonConfig:
        return self.__common

    @property
    def image(self) -> str:
        return self.__image

    @property
    def image_path(self) -> str:
        return f"{self.common.image_source}/{self.image}"

    def update_data(self, data : dict) -> None:
        """Process given data."""

        self._validate_keys(data, 'image feature options', self.__keys)

        if 'image' in data:
            self.__image = self._validate(data['image'], 'image', [self._valid_str])
        else:
            self._missing_required("'image' option of image feature")


        if 'image_source' in data:
            self.__common.image_source = self._validate(data['image_source'], 'image source', [self._valid_str])


    def __repr__(self) -> str:
        attributes : list[str] = []
        attributes.append(f"Common: {self.__common}")
        attributes.append(f"Image: {self.__image}")
        return "{" + ", ".join(attributes) + "}"
