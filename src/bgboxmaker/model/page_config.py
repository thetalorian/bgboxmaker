from bgboxmaker.model import Config, ConfigurationError
import logging
logger = logging.getLogger(__name__)

class PageConfig(Config):
    """Holds page data."""

    def __init__(self, data = {}):
        """Initialize with default data."""
        self.__keys = ['width', 'height', 'margin', 'thickness']
        self.__width : float = 11
        self.__height : float = 8.5
        self.__margin : float = 0.25
        self.__thickness : int = 4

    @property
    def width(self) -> float:
        return self.__width

    @property
    def height(self) -> float:
        return self.__height

    @property
    def margin(self) -> float:
        return self.__margin

    @property
    def thickness(self) -> int:
        return self.__thickness


    def update_data(self, data : dict) -> None:
        """Process given data."""

        self._validate_keys(data, "'page' block", self.__keys)

        if 'width' in data:
            self.__width = self._validate(data['width'], "page width", [self._valid_num, self._valid_gt_zero])

        if 'height' in data:
            self.__height = self._validate(data['height'], "page height", [self._valid_num, self._valid_gt_zero])

        if 'margin' in data:
            self.__margin = self._validate(data['margin'], "page margin", [self._valid_num, self._valid_gte_zero])

        if 'thickness' in data:
            self.__thickness = self._validate(data['thickness'], "page thickness", [self._valid_int, self._valid_gte_zero])

        self.check_orientation()


    def check_orientation(self):
        """Ensure landscape orientation."""

        if self.__height > self.__width:
            logger.warning("Page data given in portrait orientation, switching to landscape.")
            # Correct orientation
            h = self.__width
            w = self.__height
            self.__width = w
            self.__height = h
            logger.warning(f"New dimensions {self.width} by {self.height}")


    def __repr__(self) -> str:
        attributes : list[str] = []
        attributes.append(f"Width: {self.__width}")
        attributes.append(f"Height: {self.__height}")
        attributes.append(f"Margin: {self.__margin}")
        attributes.append(f"Thickness: {self.__thickness}")
        return "{" + ", ".join(attributes) + "}"