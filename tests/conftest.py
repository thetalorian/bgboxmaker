import pytest

def pytest_addoption(parser : pytest.Parser):
    parser.addoption("--images", action="store_true", default=False, help="Display test generated images.")

@pytest.fixture
def show_images(request : pytest.FixtureRequest):
    return request.config.getoption("--images")
