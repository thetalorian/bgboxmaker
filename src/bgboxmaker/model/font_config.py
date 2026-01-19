from bgboxmaker.model import Config
import logging
logger = logging.getLogger(__name__)

class FontConfig(Config):
    """Holds font configuration data."""

    def __init__(self, data : dict = {}):
        """Initialize instance with default data."""
        self.__keys = ['name', 'size', 'color', 'stroke', 'width']
        self.__name : str = "Arial.ttf"
        self.__size : int = 90
        self.__color : str = "black"
        self.__stroke : str = "white"
        self.__width : int = 1
        if data:
            self.update_data(data)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def size(self) -> int:
        return self.__size

    @size.setter
    def size(self, value : int) -> None:
        self.__size = value

    @property
    def color(self) -> str:
        return self.__color

    @property
    def stroke(self) -> str:
        return self.__stroke

    @property
    def width(self) -> int:
        return self.__width


    def _valid_ttf(self, input: str) -> bool:
        if '.' in input:
            _, ext = input.split('.')
            return ext == "ttf"
        else:
            return False


    def update_data(self, data : dict) -> None:
        """Update configuration as requested by incoming data."""

        self._validate_keys(data, "'font' block", self.__keys)

        if 'name' in data:
            self.__name = self._validate(data['name'], 'font name', [self._valid_str, self._valid_ttf])

        if 'size' in data:
            self.__size = self._validate(data['size'], 'font size', [self._valid_int, self._valid_gt_zero])

        if 'color' in data:
            self.__color = self._validate(data['color'], 'font color', [self._valid_str])

        if 'stroke' in data:
            self.__stroke = self._validate(data['stroke'], 'font stroke color', [self._valid_str])

        if 'width' in data:
            self.__width = self._validate(data['width'], 'font stroke width', [self._valid_int, self._valid_gte_zero])


    def __repr__(self) -> str:
        attributes : list[str] = []
        attributes.append(f"Name: {self.__name}")
        attributes.append(f"Size: {self.__size}")
        attributes.append(f"Color: {self.__color}")
        attributes.append(f"Stroke: {self.__stroke}")
        attributes.append(f"Width: {self.__width}")
        return "{" + ", ".join(attributes) + "}"