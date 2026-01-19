import pytest
from bgboxmaker import Box, BoxConfig

class TestBox():
    """Test code for box class."""

    @pytest.fixture()
    def box(self):
        config : BoxConfig = BoxConfig({"dimensions" : {"width": 2.5, "height" : 3.5, "depth" : 1}})
        yield Box(config)

    def test_set_page(self, box : Box) -> None:
        box._set_page()
        assert box.page.x == 3225 and box.page.y == 2475


    def test_set_box_dimensions(self, box : Box) -> None:
        box._set_box_dimensions()
        assert box.dim.x == 754 and box.dim.y == 1054 and box.dim.z == 304 and box.tabs.x == 284 and box.tabs.y == 225


    def _set_box_size(self, box : Box) -> None:
        box._set_box_size()
        assert box.size.x == 2 and box.size.y == 2