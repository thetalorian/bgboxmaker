from bgboxmaker.model import FeatureType, OptionsConfig, OptionsImageConfig, OptionsPanelConfig, OptionsTextConfig

class OptionFactory:
    """Factory class for Options"""

    @classmethod
    def get_option_class(cls, feature_type : FeatureType) -> type[OptionsConfig]:
        """Return an OptionConfig appropriate for each FeatureType"""

        options = {
            FeatureType.PANEL : OptionsPanelConfig,
            FeatureType.TEXT : OptionsTextConfig,
            FeatureType.IMAGE : OptionsImageConfig
        }

        return options[feature_type]
