
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
        message = 'The token does not have enough privilege to view: {}'.format(url)
        super().__init__(message)

class CommunicationError(Exception):
    """An HTTP error occurred"""
    def __init__(self, e):
        super().__init__(e.get_message())
