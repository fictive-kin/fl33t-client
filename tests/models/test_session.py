
import copy
import json
import requests_mock

from fl33t.models import Session


def test_create(fl33t_client):
    session_token = 'asdfasdf;lkj'

    create_response = {
        "session": {
            "admin": True,
            "device": False,
            "provisioning": False,
            "readonly": False,
            "session_token": session_token,
            "type": "api",
            "upload": False
        }
    }

    url = '/'.join((
        fl33t_client.base_team_url(),
        'session'
    ))

    with requests_mock.Mocker() as mock:
        mock.post(url, text=json.dumps(create_response))
        obj = fl33t_client.Session(
            admin=True,
            device=False,
            provisioning=False,
            readonly=False,
            upload=False,
            type='api'
        )

        response = obj.create()
        assert isinstance(response, Session)
        assert response.session_token == session_token
        assert response.priv() == 'admin'


def test_delete(fl33t_client):
    session_token = 'asdfasdf;lkj'

    get_response = {
        "session": {
            "admin": True,
            "device": False,
            "provisioning": False,
            "readonly": False,
            "session_token": session_token,
            "type": "api",
            "upload": False
        }
    }

    url = '/'.join((
        fl33t_client.base_team_url(),
        'session',
        session_token
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(get_response))
        mock.delete(url, [{'status_code': 204}])

        obj = fl33t_client.get_session(session_token)
        assert obj.delete() is True


def test_list(fl33t_client):
    list_response = {
        "session_count": 2,
        "sessions": [
            {
                "admin": True,
                "device": False,
                "provisioning": False,
                "readonly": False,
                "session_token": "asdfasdf;lkj",
                "type": "api",
                "upload": False
            },
            {
                "admin": False,
                "device": False,
                "provisioning": False,
                "readonly": True,
                "session_token": "fdsafdsajklh",
                "type": "api",
                "upload": False
            },
        ]
    }

    url = '/'.join((
        fl33t_client.base_team_url(),
        'sessions'
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(list_response))
        objs = []
        for obj in fl33t_client.list_sessions():
            assert isinstance(obj, Session)
            objs.append(obj)

        assert len(objs) == 2


def test_update(fl33t_client):

    session_token = "asdfasdf;lkj"

    update_response = {
        "session": {
            "admin": True,
            "device": False,
            "provisioning": False,
            "readonly": False,
            "session_token": session_token,
            "type": "api",
            "upload": False
        }
    }

    get_response = copy.copy(update_response)
    get_response['session']['admin'] = False
    get_response['session']['device'] = True

    url = '/'.join((
        fl33t_client.base_team_url(),
        'session',
        session_token
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(get_response))
        mock.put(url, text=json.dumps(update_response), status_code=204)

        obj = fl33t_client.get_session(session_token)
        obj.admin = True
        obj.device = False

        response = obj.update()

        assert isinstance(response, Session)
        assert response.session_token == session_token
        assert response.admin is True
        assert response.priv() == 'admin'
