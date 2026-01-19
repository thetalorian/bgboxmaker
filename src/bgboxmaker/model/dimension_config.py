from bgboxmaker.model import Config

class DimensionConfig(Config):
    """Holds box dimensions."""

    def __init__(self, data = {}):
        self.__keys : list[str] = ['width', 'height', 'depth']
        self.__width : float
        self.__height : float
        self.__depth : float
        if data:
            self.update_data(data)


    @property
    def width(self) -> float:
        return self.__width

    @property
    def height(self) -> float:
        return self.__height

    @property
    def depth(self) -> float:
        return self.__depth


    def update_data(self, data):
        """Process given data."""

        self._validate_keys(data, "'dimensions' block", self.__keys)

        if 'width' in data:
            self.__width = self._validate(data['width'], 'box width', [self._valid_num, self._valid_gt_zero])
        else:
            self._missing_required('box width')

        if 'height' in data:
            self.__height = self._validate(data['height'], 'box height', [self._valid_num, self._valid_gt_zero])
        else:
            self._missing_required('box height')

        if 'depth' in data:
            self.__depth = self._validate(data['depth'], 'box depth', [self._valid_num, self._valid_gt_zero])
        else:
            self._missing_required('box depth')

    def __repr__(self) -> str:
        attributes : list[str] = []
        attributes.append(f"Width: {self.__width}")
        attributes.append(f"Height: {self.__height}")
        attributes.append(f"Depth: {self.__depth}")
        return "{" + ", ".join(attributes) + "}"
