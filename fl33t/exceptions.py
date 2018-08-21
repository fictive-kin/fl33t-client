"""
Exceptions

All exceptions used by the fl33t client
"""


class DuplicateDeviceIdError(Exception):
    """A device by that ID already exists in fl33t."""
    pass


class InvalidIdError(Exception):
    """A generic invalid ID error that all other invalid ID errors inherit"""
    pass


class InvalidFleetIdError(InvalidIdError):
    """No fleet by that ID exists in fl33t."""
    pass


class InvalidBuildIdError(InvalidIdError):
    """No build by that ID exists in fl33t."""
    pass


class InvalidTrainIdError(InvalidIdError):
    """No train by that ID exists in fl33t."""
    pass


class InvalidDeviceIdError(InvalidIdError):
    """No device by that ID exists in fl33t."""
    pass


class InvalidSessionIdError(InvalidIdError):
    """No session by that ID exists in fl33t."""
    pass


class UnprivilegedToken(Exception):
    """The token in use is not privileged for the URL used"""

    _message = 'The token does not have enough privilege to view: {}'

    def __init__(self, url):
        super().__init__(self._message.format(url))


class Fl33tApiException(Exception):
    """The fl33t API returned an exception handling our request"""
    pass


class Fl33tClientException(Exception):
    """A model has been instantiated without providing an API client"""
    pass
