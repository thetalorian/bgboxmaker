from bgboxmaker.model import Config


class BasicConfig(Config):
    """Holds data for basic tuck box."""

    def __init__(self, data = {}):
        self.__keys : list[str] = ['title', 'subtitle', 'extra']
        self.__title : str = ""
        self.__subtitle : str = ""
        self.__extra : str = ""
        if data:
            self.update_data(data)

    @property
    def title(self) -> str:
        return self.__title

    @property
    def subtitle(self) -> str:
        return self.__subtitle

    @property
    def extra(self) -> str:
        return self.__extra

    @property
    def isSet(self) -> bool:
        return self.__title != "" or self.__extra != ""

    def update_data(self, data):
        """Process given data."""

        self._validate_keys(data, "'basic' block", self.__keys)

        if 'title' in data:
            self.__title = self._validate(data['title'], 'title', [self._valid_str])

        if 'subtitle' in data:
            self.__subtitle = self._validate(data['subtitle'], 'subtitle', [self._valid_str])

        if 'extra' in data:
            self.__extra = self._validate(data['extra'], 'extra', [self._valid_str])

    def __repr__(self) -> str:
        attributes : list[str] = []
        attributes.append(f"title: {self.__title}")
        attributes.append(f"subtitle: {self.__subtitle}")
        attributes.append(f"extra: {self.__extra}")
        return "{" + ", ".join(attributes) + "}"
