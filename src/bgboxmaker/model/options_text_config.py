from bgboxmaker.model import CommonConfig, OptionsConfig, FontConfig, ConfigurationError
import logging
logger = logging.getLogger(__name__)

class OptionsTextConfig(OptionsConfig):
    """Holds options for Text Feature."""

    def __init__(self, common : CommonConfig, data : dict = {}):
        self.__keys : list[str] = ['text', 'align', 'font']
        self.__common : CommonConfig = common
        self.__text : str = ""
        self.__align : str = "center"
        if data:
            self.update_data(data)

    @property
    def common(self) -> CommonConfig:
        return self.__common

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, value : str) -> None:
        self.__text = value

    @property
    def align(self) -> str:
        return self.__align

    @align.setter
    def align(self, value : str) -> None:
        self.__align = value

    def _valid_multiline(self, lines : list) -> bool:
        """Validate that provided list is list of str."""
        valid = True
        for s in lines:
            valid = valid and isinstance(s, str)
        return valid


    def _valid_align(self, input : str) -> bool:
        return input in ['left', 'center', 'right', 'justified']


    def update_data(self, data):
        """Process given data."""

        self._validate_keys(data, 'text feature options', self.__keys)

        if 'text' in data:
            if isinstance(data['text'], list):
                text = self._validate(data['text'], 'feature text', [self._valid_multiline])
                self.__text = "\n".join(text)
            else:
                self.__text = self._validate(data['text'], 'feature text', [self._valid_str])
        else:
            self._missing_required("'text' option of text feature")

        if 'align' in data:
            self.__align = self._validate(data['align'], 'feature text align', [self._valid_str, self._valid_align])

        if 'font' in data:
            self._found('font')
            self.__common.font.update_data(data['font'])


    def __repr__(self) -> str:
        attributes : list[str] = []
        attributes.append(f"Common: {self.__common}")
        attributes.append(f"Text: {self.__text}")
        attributes.append(f"Align: {self.__align}")
        return "{" + ", ".join(attributes) + "}"
