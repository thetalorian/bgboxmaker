from bgboxmaker.dim import Dim
import logging
logger = logging.getLogger(__name__)


class FeatureGrid:
    """Object representing a placement grid for section features.

    Attributes
    ----------
    lines : Dim
        Number of grid lines, horizontal and vertical
    area : Dim
        Width and height of area overlaid by the grid
    margin : int
        Margin (in pixels) around the grid on the given area.
    x : list
        List of horizontal grid positions
    y : list
        List of vertical grid positions
    """

    def __init__(self, lines : Dim, area : Dim, margin : int):
        if lines.x > 0 and lines.y > 0:
            self.__lines : Dim = lines
        else:
            logger.error("Grid must be at least 1 x 1. Requested: {lines.x} by {lines.y}")
            raise ValueError
        self.__area : Dim = area
        self.__margin : int = margin
        self.__x : list = []
        self.__y : list = []
        self._set_locations()


    def _set_locations(self) -> None:
        """Generate grid locations."""
        usable_area = Dim(self.__area.x - self.__margin * 2, self.__area.y - self.__margin * 2)

        # Assign positions based on print area, should leave
        # margin amount of space around the equally spaced grid.
        for x in range(self.__lines.x + 1):
            self.__x.append(int(usable_area.x / self.__lines.x) * x + self.__margin)
        for y in range(self.__lines.y + 1):
            self.__y.append(int(usable_area.y / self.__lines.y) * y + self.__margin)


    def get_pos(self, location : Dim) -> Dim:
        """Return pixel coordinates for given grid location"""
        if location.x > self.__lines.x or location.y > self.__lines.y:
            logger.error(f"Requested location ({location}) invalid for grid of size {self.__lines}")
            raise ValueError
        return Dim(self.__x[location.x], self.__y[location.y])
