import pytest
from bgboxmaker import BoxConfig, SectionName, ConfigurationError, FeatureType, Dim

class TestSectionConfig():
    """Test code for SectionConfig class"""

    @pytest.fixture()
    def data(self):
        yield  {"dimensions" : {"width" : 2.5, "height" : 3.5, "depth" : 1}}

    @pytest.fixture()
    def config(self, data : dict):
        config : BoxConfig = BoxConfig(data)
        yield config


    def test_repr(self, data : dict, config : BoxConfig) -> None:
        section_data = {"front" : {}}
        data['detail'] = section_data
        config.update_data(data)
        print(config)


    def test_update_data_dimensions(self, data : dict, config : BoxConfig) -> None:
        data['dimensions'] = {"width" : 1, "height" : 1.5, "depth" : 0.5}
        config.update_data(data)
        assert config.dimensions.width == 1


    def test_update_data_dimensions_missing(self, config : BoxConfig) -> None:
        with pytest.raises(ConfigurationError):
            config.update_data({})

    def test_update_data_page(self, data : dict, config : BoxConfig) -> None:
        data['page'] = {"width" : 14}
        config.update_data(data)
        assert config.page.width == 14


    def test_update_data_common(self, data : dict, config : BoxConfig) -> None:
        data['common'] = {"image_source" : "path"}
        config.update_data(data)
        assert config.common.image_source == "path"


    def test_update_data_background(self, data : dict, config : BoxConfig) -> None:
        data['background'] = {"color" : "red"}
        config.update_data(data)
        assert config.background.color == "red"


    def test_update_data_basic(self, data : dict, config : BoxConfig) -> None:
        data['basic'] = {"title" : "title"}
        config.update_data(data)
        assert config.basic.title == "title"


    def test_update_data_detail_sides(self, data : dict, config : BoxConfig) -> None:
        data['detail'] = {"sides" : {}}
        config.update_data(data)
        assert config.detail[SectionName.LEFT] and config.detail[SectionName.RIGHT]


    def test_update_data_detail_ends(self, data : dict, config : BoxConfig) -> None:
        data['detail'] = {"ends" : {}}
        config.update_data(data)
        assert config.detail[SectionName.TOP] and config.detail[SectionName.BOTTOM]


    def test_update_data_detail_faces(self, data : dict, config : BoxConfig) -> None:
        data['detail'] = {"faces" : {}}
        config.update_data(data)
        assert config.detail[SectionName.FRONT] and config.detail[SectionName.BACK]


    def test_add_basic_blank_title(self, data : dict, config : BoxConfig) -> None:
        data['basic'] = {'title' : 'title'}
        config.update_data(data)
        front_title = config.detail[SectionName.FRONT].features[0].options.text == "title" # type: ignore
        left_title = config.detail[SectionName.LEFT].features[0].options.text == "title" # type: ignore
        grid = config.detail[SectionName.FRONT].grid == Dim(2, 4)
        assert front_title and left_title and grid


    def test_add_basic_blank_subtitle(self, data : dict, config : BoxConfig) -> None:
        data['basic'] = {'title' : 'title', 'subtitle' : 'subtitle'}
        config.update_data(data)
        front_title = config.detail[SectionName.FRONT].features[0].options.text == "title" # type: ignore
        front_subtitle = config.detail[SectionName.FRONT].features[1].options.text == "subtitle" # type: ignore
        left_title = config.detail[SectionName.LEFT].features[0].options.text == "title: subtitle" # type: ignore
        grid = config.detail[SectionName.FRONT].grid == Dim(2, 7)
        assert front_title and front_subtitle and left_title and grid


    def test_add_basic_blank_extra(self, data : dict, config : BoxConfig) -> None:
        data['basic'] = {'extra' : '1'}
        config.update_data(data)
        front_extra = config.detail[SectionName.FRONT].features[0].options.text == "1" # type: ignore
        assert front_extra


    def test_add_basic_section_title(self, data : dict, config : BoxConfig) -> None:
        data['basic'] = {'title': 'title'}
        data['detail'] = {}
        data['detail']['front'] = {}
        config.update_data(data)
        front_title = config.detail[SectionName.FRONT].features[0].options.text == "title" # type: ignore
        assert front_title


    def test_add_basic_section_feature_title(self, data : dict, config : BoxConfig) -> None:
        data['basic'] = {'title': 'title'}
        data['detail'] = {}
        data['detail']['front'] = {}
        data['detail']['front']['features'] = [{'type' : 'text', 'options': {'text': 'other'}}]
        config.update_data(data)
        front_title = config.detail[SectionName.FRONT].features[0].options.text == "title" # type: ignore
        assert not front_title

