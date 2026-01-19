import pytest
from bgboxmaker.dim import Dim
from bgboxmaker.view import FeatureGrid


class TestFeatureGrid():
    """Test code for FeatureGrid class."""

    @pytest.fixture()
    def grid(self):
        yield FeatureGrid(Dim(2, 2), Dim(100, 200), 10)

    @pytest.fixture()
    def grid2(self):
        yield FeatureGrid(Dim(1, 3), Dim(100, 200), 10)


    def test_grid_invalid(self) -> None:
        with pytest.raises(ValueError):
            grid = FeatureGrid(Dim(0,0), Dim(100, 200), 10)


    def test_grid_location_0_0(self, grid : FeatureGrid) -> None:
        assert grid.get_pos(Dim(0,0)) == Dim(10, 10)


    def test_grid_location_1_0(self, grid : FeatureGrid) -> None:
        assert grid.get_pos(Dim(1,0)) == Dim(50, 10)


    def test_grid_location_2_2(self, grid : FeatureGrid) -> None:
        assert grid.get_pos(Dim(2,2)) == Dim(90, 190)


    def test_grid2_location_0_0(self, grid2 : FeatureGrid) -> None:
        assert grid2.get_pos(Dim(0,0)) == Dim(10, 10)


    def test_grid2_location_1_0(self, grid2 : FeatureGrid) -> None:
        assert grid2.get_pos(Dim(1,0)) == Dim(90, 10)


    def test_grid2_location_1_2(self, grid2 : FeatureGrid) -> None:
        assert grid2.get_pos(Dim(1,2)) == Dim(90, 130)


    def test_grid2_location_2_2(self, grid2 : FeatureGrid) -> None:
        with pytest.raises(ValueError):
            pos = grid2.get_pos(Dim(2,2))






