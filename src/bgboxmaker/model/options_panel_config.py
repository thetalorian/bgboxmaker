from bgboxmaker.model import CommonConfig, OptionsConfig

class OptionsPanelConfig(OptionsConfig):
    """Holds options for Panel Feature."""

    def __init__(self, common : CommonConfig, data : dict):
        self.__keys : list[str] = ['color', 'border', 'border_width']
        self.__common : CommonConfig = common
        self.__color : str = "gray"
        self.__border : str = "gray"
        self.__border_width : int = 0
        if data:
            self.update_data(data)

    @property
    def color(self) -> str:
        return self.__color

    @property
    def border(self) -> str:
        return self.__border

    @property
    def border_width(self) -> int:
        return self.__border_width

    def update_data(self, data):
        """Process given data."""

        self._validate_keys(data, 'panel feature options', self.__keys)

        if 'color' in data:
            self.__color = self._validate(data['color'], 'panel color', [self._valid_str])

        if 'border' in data:
            self.__border = self._validate(data['border'], 'panel border', [self._valid_str])

        if 'border_width' in data:
            self.__border_width = self._validate(data['border_width'], 'panel border width', [self._valid_int])


    def __repr__(self) -> str:
        attributes : list[str] = []
        attributes.append(f"Common: {self.__common}")
        attributes.append(f"Color: {self.__color}")
        attributes.append(f"Border Color: {self.__border}")
        attributes.append(f"Border Width: {self.__border_width}")
        return "{" + ", ".join(attributes) + "}"