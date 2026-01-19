class ConfigurationError(Exception):
    """General use exception for configuration errors."""

    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)