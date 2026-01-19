from bgboxmaker.dim import Dim
from bgboxmaker.model import Config, CommonConfig, BackgroundConfig, ConfigurationError, Orientation, FeatureType, OptionFactory, OptionsConfig
import logging
logger = logging.getLogger(__name__)


class FeatureConfig(Config):
    """Holds feature configuration data."""

    def __init__(self, common : CommonConfig, data : dict = {}):
        self.__keys : list[str] = ['type', 'options', 'width', 'height', 'place', 'anchor']
        self.__common : CommonConfig = common
        self.__type : FeatureType = None
        self.__options : OptionsConfig = None
        self.__width : float = 0
        self.__height : float = 0
        self.__place : Dim = Dim(1,1)
        self.__anchor : Dim = Dim(1,1)
        if data:
            self.update_data(data)

    @property
    def common(self) -> CommonConfig:
        return self.__common

    @property
    def type(self) -> FeatureType:
        return self.__type

    @type.setter
    def type(self, value : FeatureType) -> None:
        self.__type = value

    @property
    def options(self) -> OptionsConfig:
        return self.__options

    @options.setter
    def options(self, value : OptionsConfig) -> None:
        self.__options = value

    @property
    def width(self) -> float:
        return self.__width

    @property
    def height(self) -> float:
        return self.__height

    @property
    def place(self) -> Dim:
        return self.__place

    @place.setter
    def place(self, value : Dim) -> None:
        self.__place = value

    @property
    def anchor(self) -> Dim:
        return self.__anchor

    @anchor.setter
    def anchor(self, value : Dim) -> None:
        self.__anchor = value

    def _valid_zero_to_two(self, input) -> bool:
        """Validate all list members are between 0 and 2"""
        return input[0] in [0, 1, 2] and input[1] in [0, 1, 2]


    def update_data(self, data):
        """Process given data."""

        self._validate_keys(data, "'feature' block", self.__keys)

        if 'type' in data:
            feature_type = self._validate(data['type'], 'feature type', [self._valid_str])
            self.__type = self._validate_enum(feature_type, 'feature type', FeatureType)
        else:
            self._missing_required('feature type')

        if 'options' in data:
            self._found('Option data')
            option_class : type[OptionsConfig] = OptionFactory.get_option_class(self.__type)
            self.__options = option_class(self.__common, data['options'])

        if 'width' in data:
            self.__width = self._validate(data['width'], 'feature width', [self._valid_num, self._valid_gt_zero])

        if 'height' in data:
            self.__height = self._validate(data['height'], 'feature height', [self._valid_num, self._valid_gt_zero])

        if 'place' in data:
            self.__place = Dim(self._validate(data['place'], 'place', [self._valid_list, self._valid_Vec2_int]))

        if 'anchor' in data:
            self.__anchor = Dim(self._validate(data['anchor'], 'anchor', [self._valid_list, self._valid_Vec2_int, self._valid_zero_to_two]))


    def __repr__(self) -> str:
        attributes : list[str] = []
        attributes.append(f"Common: {self.__common}")
        attributes.append(f"Type: {self.__type}")
        attributes.append(f"Options: {self.__options}")
        attributes.append(f"Width: {self.__width}")
        attributes.append(f"Height {self.__height}")
        attributes.append(f"Place: {self.__place}")
        attributes.append(f"Anchor: {self.__anchor}")
        return "{" + "\n".join(attributes) + "}"