from bgboxmaker.dim import Dim
from bgboxmaker.model import Config, BasicConfig, CommonConfig, DimensionConfig, PageConfig
from bgboxmaker.model import SectionConfig, BackgroundConfig, SectionName, FeatureConfig, FeatureType, OptionsTextConfig
import logging
logger = logging.getLogger(__name__)


class BoxConfig(Config):
    """Holds box configuration converted from YAML file."""

    def __init__(self, data = {}):
        super(Config, self).__init__()
        self.__keys : list[str] = ['dimensions', 'page', 'background', 'common', 'basic', 'detail']
        self.__dimensions : DimensionConfig
        self.__page : PageConfig = PageConfig()
        self.__common : CommonConfig = CommonConfig()
        self.__background : BackgroundConfig = BackgroundConfig(self.__common)
        self.__detail : dict[SectionName, SectionConfig] = {}
        self.__basic : BasicConfig = BasicConfig()
        if data:
            self.update_data(data)

    @property
    def dimensions(self) -> DimensionConfig:
        return self.__dimensions

    @property
    def page(self) -> PageConfig:
        return self.__page

    @property
    def common(self) -> CommonConfig:
        return self.__common

    @property
    def background(self) -> BackgroundConfig:
        return self.__background

    @property
    def detail(self) -> dict[SectionName, SectionConfig]:
        return self.__detail

    @property
    def basic(self) -> BasicConfig:
        return self.__basic

    def update_data(self, data):
        """Process given data."""

        self._validate_keys(data, 'config', self.__keys)

        if 'dimensions' in data:
            self._found("dimensions")
            self.__dimensions = DimensionConfig(data['dimensions'])
        else:
            self._missing_required("Dimensions")

        if 'page' in data:
            self._found("page")
            self.__page.update_data(data['page'])

        if 'common' in data:
            self._found('common')
            self.__common.update_data(data['common'])

        if 'background' in data:
            self._found('background')
            self.__background = BackgroundConfig(self.__common, data['background'])

        if 'basic' in data:
            self._found('basic')
            self.__basic = BasicConfig(data['basic'])

        if 'detail' in data:
            self._found('detail')
            sides = [SectionName.LEFT, SectionName.RIGHT]
            ends = [SectionName.TOP, SectionName.BOTTOM]
            faces = [SectionName.FRONT, SectionName.BACK]
            for detail in data['detail']:
                section = self._validate_enum(detail, 'detail', SectionName)
                if section == SectionName.SIDES:
                    for s in sides:
                        if s not in self.__detail:
                            self.__detail[s] = SectionConfig(self.common, data['detail'][detail])
                if section == SectionName.ENDS:
                    for s in ends:
                        if s not  in self.__detail:
                            self.__detail[s] = SectionConfig(self.common, data['detail'][detail])
                if section == SectionName.FACES:
                    for s in faces:
                        if s not in self.__detail:
                            self.__detail[s] = SectionConfig(self.common, data['detail'][detail])
                self.__detail[section] = SectionConfig(self.common, data['detail'][detail])

        if self.__basic.isSet:
            self._add_basic_box_features()

    def _add_basic_box_features(self):
        """Populate box sections with config from 'basic' block."""
        for section in [SectionName.FRONT, SectionName.LEFT, SectionName.RIGHT, SectionName.TOP, SectionName.BOTTOM]:
            if section not in self.__detail:
                logger.info(f"No existing configuration found for {section}, creating.")
                self.__detail[section] = SectionConfig(self.common)
            else:
                logger.info(f"Existing configuration found for {section} section, editing.")
            detail = self.__detail[section]
            if not detail.features:
                logger.info(f"No features found for {section}. Generating.")
                if section is SectionName.FRONT:
                    self._add_front_features(detail)
                else:
                    self._add_side_features(detail)
            else:
                logger.info(f"Existing features found in {section}, skipping.")


    def _add_front_features(self, detail : SectionConfig):
        """Create basic features for Front Section.

        If title is assigned, display toward the top of the front side.
        If subtitle is also assigned, display slightly lower, at a slightly smaller font.
        If extra text is provided, place it at the bottom of the section.
        """
        if self.__basic.title and self.__basic.subtitle:
            div = 7
        else:
            div = 4

        detail.grid = Dim(2, div)

        if self.__basic.title:
            logger.info("Adding title info to Front section.")
            title_feature = FeatureConfig(detail.common)
            title_feature.type = FeatureType.TEXT
            title_feature.place = Dim(1, 1)
            title_feature.options = OptionsTextConfig(detail.common)
            title_feature.options.text = self.__basic.title
            detail.features.append(title_feature)

        if self.__basic.subtitle:
            logger.info("Adding subtitle info to Front section.")
            subtitle_feature = FeatureConfig(detail.common)
            subtitle_feature.type = FeatureType.TEXT
            subtitle_feature.place = Dim(1, 2)
            subtitle_feature.options = OptionsTextConfig(detail.common)
            subtitle_feature.options.text = self.__basic.subtitle
            subtitle_feature.options.common.font.size = 70
            detail.features.append(subtitle_feature)

        if self.__basic.extra:
            logger.info("Adding extra text to Front section.")
            extra_feature = FeatureConfig(detail.common)
            extra_feature.type = FeatureType.TEXT
            extra_feature.place = Dim(1, div)
            extra_feature.anchor = Dim(1, 2)
            extra_feature.options = OptionsTextConfig(detail.common)
            extra_feature.options.text = self.__basic.extra
            extra_feature.options.common.font.size = 50
            detail.features.append(extra_feature)


    def _add_side_features(self, detail : SectionConfig):
        """Add basic features for side and end sections.

        If title is assigned, add title text to sides and ends.
        If subtitle is also assigned, append to title with ":".
        """

        if self.__basic.title:
            logger.info("Adding title to section.")
            if self.__basic.subtitle:
                text = ": ".join((self.__basic.title, self.__basic.subtitle))
            else:
                logger.info("Adding subtitle to section.")
                text = self.__basic.title
            title_feature = FeatureConfig(detail.common)
            title_feature.type = FeatureType.TEXT
            title_feature.place = Dim(1, 1)
            title_feature.options = OptionsTextConfig(detail.common)
            title_feature.options.text = text
            title_feature.options.align = "left"
            title_feature.common.font.size = 50
            detail.features.append(title_feature)


    def __repr__(self) -> str:
        attributes : list[str] = []
        attributes.append(f"Dimensions: {self.__dimensions}")
        attributes.append(f"Page: {self.__page}")
        attributes.append(f"Common: {self.__common}")
        attributes.append(f"Background: {self.__background}")
        attributes.append(f"Basic: {self.__basic}")
        attributes.append(f"Detail:")
        for section in self.__detail:
            attributes.append(f"{section}")
            attributes.append(f"{self.__detail[section]}")
        self.__detail : dict[SectionName, SectionConfig] = {}
        return "{" + "\n".join(attributes) + "}"