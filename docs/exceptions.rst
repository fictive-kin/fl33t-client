Exceptions
==========

These are the exceptions in use within the fl33t module.

Generic Exceptions
------------------

.. autoclass:: fl33t.exceptions.UnprivilegedToken

    :param str url: The URL that access to was forbidden by fl33t

.. autoclass:: fl33t.exceptions.Fl33tApiException

.. autoclass:: fl33t.exceptions.Fl33tClientException


Build Exceptions
----------------

.. autoclass:: fl33t.exceptions.InvalidBuildIdError


Device Exceptions
-----------------

.. autoclass:: fl33t.exceptions.InvalidDeviceIdError

.. autoclass:: fl33t.exceptions.DuplicateDeviceIdError

Fleet Exceptions
----------------

.. autoclass:: fl33t.exceptions.InvalidFleetIdError

Train Exceptions
----------------

.. autoclass:: fl33t.exceptions.InvalidTrainIdError

Session Exceptions
------------------

.. autoclass:: fl33t.exceptions.InvalidSessionIdError

