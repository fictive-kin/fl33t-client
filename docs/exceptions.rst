Exceptions
==========

These are the exceptions in use within the fl33t module.

Generic
-------

.. autoclass:: fl33t.exceptions.UnprivilegedToken

    :param str url: The URL that access to was forbidden to by fl33t

.. autoclass:: fl33t.exceptions.Fl33tApiException

.. autoclass:: fl33t.exceptions.Fl33tClientException


Model Related
-------------

.. autoclass:: fl33t.exceptions.DuplicateDeviceIdError

.. autoclass:: fl33t.exceptions.InvalidDeviceIdError

.. autoclass:: fl33t.exceptions.InvalidBuildIdError

.. autoclass:: fl33t.exceptions.BuildUploadError

.. autoclass:: fl33t.exceptions.NoUploadUrlProvidedError

.. autoclass:: fl33t.exceptions.InvalidFleetIdError

.. autoclass:: fl33t.exceptions.InvalidTrainIdError

.. autoclass:: fl33t.exceptions.InvalidSessionIdError


Base Exceptions
---------------

.. autoclass:: fl33t.exceptions.InvalidIdError
