
import json
import pytest
import requests_mock

from fl33t.exceptions import InvalidSessionIdError
from fl33t.models import Session


def test_own_session(fl33t_client):
    session_response = {
        'session': {
            'admin': False,
            'device': False,
            'provisioning': False,
            'readonly': False,
            'session_token': fl33t_client.token,
            'type': 'api',
            'upload': True
        }
    }

    url = '/'.join((
        fl33t_client.base_team_url(),
        'session',
        fl33t_client.token
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(session_response))

        obj = fl33t_client.get_own_session()

        assert isinstance(obj, Session)
        assert obj.session_token == fl33t_client.token
        assert obj.priv() == 'upload'


def test_fail_get_session_invalid_id(fl33t_client):
    session_token = 'asdffdsa'

    url = '/'.join((
        fl33t_client.base_team_url(),
        'session',
        session_token
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, [
            {'status_code': 400, 'text': 'Invalid session token'},
            {'status_code': 404, 'text': 'Page not found'}
        ])

        with pytest.raises(InvalidSessionIdError):
            obj = fl33t_client.get_session(session_token)
            obj = fl33t_client.get_session(session_token)
