Reference
=========

.. autoclass:: fl33t.Fl33tClient
    :members:

    :param str team_id: The fl33t team ID for your account
    :param str session_token: The fl33t session token you would like to connect as
    :param str base_uri: The base URL to use for fl33t interactions. Defaults to https://api.fl33t.com
    :param int generated_id_length: The length of any generated device IDs. Defaults to 6
    :param int default_query_limit: The max results to return for any lists of fl33t objects when no offset is specifically used
