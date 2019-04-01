
import copy
import json
import requests_mock

from fl33t.models import Session


def test_create(fl33t_client):
    session_token = 'asdfasdf;lkj'

    create_response = {
        "session": {
            "name": "My Session Name",
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
        fl33t_client.base_team_url,
        'session'
    ))

    with requests_mock.Mocker() as mock:
        mock.post(url, text=json.dumps(create_response))
        obj = fl33t_client.Session(
            name="My Session Name",
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
        assert response.id == session_token
        assert response.priv == 'admin'
        assert str(response) == 'Session {} (Type: {} Privilege: {})'.format(
            'My Session Name',
            'api',
            'admin'
        )
        assert repr(response) == '<Session name={} type={} priv={}>'.format(
            'My Session Name',
            'api',
            'admin'
        )


def test_delete(fl33t_client):
    session_token = 'asdfasdf;lkj'

    get_response = {
        "session": {
            "name": "My Session Name",
            "admin": False,
            "device": False,
            "provisioning": False,
            "readonly": False,
            "session_token": session_token,
            "type": "api",
            "upload": False
        }
    }

    url = '/'.join((
        fl33t_client.base_team_url,
        'session',
        session_token
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(get_response))
        mock.delete(url, [{'status_code': 204}])

        obj = fl33t_client.get_session(session_token)
        assert obj.priv == 'unprivileged'
        assert obj.delete() is True


def test_list(fl33t_client):
    list_response = {
        "session_count": 3,
        "sessions": [
            {
                "name": "My First Session",
                "admin": False,
                "device": False,
                "provisioning": True,
                "readonly": False,
                "session_token": "asdfasdf;lkj",
                "type": "api",
                "upload": False
            },
            {
                "name": "My Second Session",
                "admin": False,
                "device": False,
                "provisioning": False,
                "readonly": True,
                "session_token": "fdsafdsajklh",
                "type": "api",
                "upload": False
            },
            {
                "name": "My Third Session",
                "admin": False,
                "device": False,
                "provisioning": False,
                "readonly": False,
                "session_token": "psdfgertkkj",
                "type": "api",
                "upload": True
            },
        ]
    }

    url = '/'.join((
        fl33t_client.base_team_url,
        'sessions'
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(list_response))
        objs = []
        for obj in fl33t_client.list_sessions():
            assert isinstance(obj, Session)
            objs.append(obj)

        assert len(objs) == 3
        assert objs[0].priv == 'provisioning'
        assert objs[1].priv == 'readonly'
        assert objs[2].priv == 'upload'


def test_update(fl33t_client):

    session_token = "asdfasdf;lkj"

    update_response = {
        "session": {
            "name": "My Session Name",
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
        fl33t_client.base_team_url,
        'session',
        session_token
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(get_response))
        mock.put(url, text=json.dumps(update_response), status_code=204)

        obj = fl33t_client.get_session(session_token)
        assert obj.priv == 'device'

        obj.admin = True
        obj.device = False

        response = obj.update()

        assert isinstance(response, Session)
        assert response.session_token == session_token
        assert response.admin is True
        assert response.priv == 'admin'


def test_session_json(fl33t_client):
    session_token = 'asdfasdf;lkj'

    get_response = {
        "session": {
            "name": "My Session Name",
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
        fl33t_client.base_team_url,
        'session',
        session_token
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(get_response))

        obj = fl33t_client.get_session(session_token)

        json_data = obj.to_json()
        assert json_data == json.dumps(get_response)
