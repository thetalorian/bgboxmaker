from enum import Enum

class SectionName(Enum):
    """Enum class for section names."""
    GLUE_TAB = 0
    BACK = 1
    LEFT = 2
    FRONT = 3
    RIGHT = 4
    BOTTOM = 5
    BOTTOM_TAB = 6
    TOP = 7
    TOP_TAB = 8
    LT_TAB = 9
    RT_TAB = 10
    LB_TAB = 11
    RB_TAB = 12
    SIDES = 13
    ENDS = 14
    FACES = 15

class SectionType(Enum):
    """Enum class for section types. Used to adjust the shape of rendered image."""
    PANE =0
    BACK = 1
    GLUE_TAB = 2
    SIDE_TAB = 3
    TUCK_TAB = 4

class FeatureType(Enum):
    """Enum class for feature types."""
    PANEL = 0
    TEXT = 1
    IMAGE = 2

class Orientation(Enum):
    """Enum class for section orientations."""
    PORTRAIT = 1
    LANDSCAPE = 2

