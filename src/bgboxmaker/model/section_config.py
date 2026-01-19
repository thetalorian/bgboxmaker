from bgboxmaker.dim import Dim
from bgboxmaker.model import Config, CommonConfig, BackgroundConfig, FeatureConfig, Orientation

class SectionConfig(Config):
    """Holds detail section config."""

    def __init__(self, common : CommonConfig, data : dict = {}):
        self.__keys : list[str] = ['background', 'rotated', 'orientation', 'margin', 'grid', 'features']
        self.__common : CommonConfig = common
        self.__background : BackgroundConfig = BackgroundConfig(common)
        self.__rotated : bool = False
        self.__rotated_is_set : bool = False
        self.__orientation : Orientation = Orientation.LANDSCAPE
        self.__orientation_is_set : bool = False
        self.__grid : Dim = Dim(2, 2)
        self.__features : list[FeatureConfig] = []
        if data:
            self.update_data(data)

    @property
    def common(self) -> CommonConfig:
        return self.__common

    @property
    def background(self) -> BackgroundConfig:
        return self.__background

    @property
    def rotated(self) -> bool:
        return self.__rotated

    @property
    def rotated_is_set(self) -> bool:
        return self.__rotated_is_set

    @property
    def orientation(self) -> Orientation:
        return self.__orientation

    @property
    def orientation_is_set(self) -> bool:
        return self.__orientation_is_set

    @property
    def grid(self) -> Dim:
        return self.__grid

    @grid.setter
    def grid(self, value : Dim) -> None:
        self.__grid = value

    @property
    def features(self) -> list[FeatureConfig]:
        return self.__features


    def update_data(self, data):
        """Update given data."""

        self._validate_keys(data, "'detail' block", self.__keys)

        if 'background' in data:
            self._found('background')
            self.__background = BackgroundConfig(self.__common, data['background'])

        if 'rotated' in data:
            self.__rotated = self._validate(data['rotated'], 'rotated', [self._valid_bool])
            self.__rotated_is_set = True

        if 'orientation' in data:
            orientation = self._validate(data['orientation'], 'orientation', [self._valid_str])
            self.__orientation = self._validate_enum(orientation, 'orientation', Orientation)
            self.__orientation_is_set = True

        if 'margin' in data:
            self.__common.margin = self._validate(data['margin'], 'margin', [self._valid_num, self._valid_gte_zero])

        if 'grid' in data:
            self.__grid = Dim(self._validate(data['grid'], 'grid', [self._valid_list, self._valid_Vec2_int, self._valid_Vec2_gt_zero]))

        if 'features' in data:
            self._found('features')
            for feature in data['features']:
                self.__features.append(FeatureConfig(self.__common, feature))


    def __repr__(self) -> str:
        attributes: list[str] = []
        attributes.append(f"Common: {self.__common}")
        attributes.append(f"Background: {self.__background}")
        attributes.append(f"Rotated: {self.__rotated}")
        attributes.append(f"Orientation: {self.__orientation}")
        attributes.append(f"Grid: {self.__grid}")
        for feature in self.__features:
            attributes.append("Feature:")
            attributes.append(f"{feature}")
            attributes.append("")
        return "\n".join(attributes)