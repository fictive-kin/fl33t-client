"""
Exceptions

All exceptions used by the fl33t client
"""


class DuplicateDeviceIdError(Exception):
    """A device by that ID already exists in Fleet."""
    pass


class InvalidFleetIdError(Exception):
    """No fleet by that ID exists in Fleet."""
    pass


class InvalidBuildIdError(Exception):
    """No build by that ID exists in Fleet."""
    pass


class InvalidTrainIdError(Exception):
    """No train by that ID exists in Fleet."""
    pass


class InvalidDeviceIdError(Exception):
    """No device by that ID exists in Fleet."""
    pass


class InvalidSessionIdError(Exception):
    """No session by that ID exists in Fleet."""
    pass


class UnprivilegedToken(Exception):
    """The token in use is not privileged for the URL used"""

    _message = 'The token does not have enough privilege to view: {}'

    def __init__(self, url):
        super().__init__(self._message.format(url))


class Fl33tApiException(Exception):
    """The Fl33t API returned an exception handling our request"""
    pass


class Fl33tClientException(Exception):
    """A model has been instantiated without providing an API client"""
    pass
