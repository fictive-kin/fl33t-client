
class DuplicateDeviceIdError(Exception):
    """A device by that ID already exists in Fleet."""
    pass

class InvalidDeviceIdError(Exception):
    """A device by that ID already exists in Fleet."""
    pass

class InvalidSessionIdError(Exception):
    """A device by that ID already exists in Fleet."""
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
