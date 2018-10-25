
import pytest
import requests_mock

from fl33t.exceptions import (
    Fl33tApiException,
    Fl33tClientException,
    UnprivilegedToken
)
from fl33t.models import Session


def test_fail_unprivileged(fl33t_client):
    session_token = 'asdffdsa'

    url = '/'.join((
        fl33t_client.base_team_url,
        'session',
        session_token
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, [
            {'status_code': 401, 'text': 'Login required'},
            {'status_code': 403, 'text': 'Forbidden'}
        ])

        with pytest.raises(UnprivilegedToken):
            fl33t_client.get_session(session_token)
            fl33t_client.get_session(session_token)


def test_fl33t_api_failure(fl33t_client):
    session_token = 'asdffdsa'

    url = '/'.join((
        fl33t_client.base_team_url,
        'session',
        session_token
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, [
            {'status_code': 500, 'text': 'Internal Server Error'},
            {'status_code': 502, 'text': 'Gateway Timeout'}
        ])

        with pytest.raises(Fl33tApiException):
            fl33t_client.get_session(session_token)
            fl33t_client.get_session(session_token)


def test_fl33t_client_exc():

    session = Session(session_token='asdffdsa')

    with pytest.raises(Fl33tClientException):
        session.create()
