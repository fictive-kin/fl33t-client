
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
    def __init__(self, url):
        message = 'The token does not have enough privilege to view: {}'.format(
                url)
        super().__init__(message)


class Fl33tApiException(Exception):
    """The Fl33t API returned an exception handling our request"""
    def __init__(self, url, status_code, message):
        message = 'The Fl33t API returned an error for: {} : {} - {}'.format(
                url, status_code, message)
        super().__init__(message)
