
import copy
import json
import requests_mock

from fl33t.models import Device, Build


def test_create(fl33t_client):
    device_id = 'asdf'
    fleet_id = 'fdsa'
    name = 'My Device'
    session_token = 'poiuytrewq'

    create_response = {
        "device": {
            "build_id": None,
            "checkin_tstamp": "2018-03-31T22:31:08.836406Z",
            "device_id": device_id,
            "name": name,
            "fleet_id": fleet_id,
            "session_token": session_token
        }
    }

    url = '{}/team/{}/device'.format(
            fl33t_client.base_uri, fl33t_client.team_id)

    with requests_mock.Mocker() as mock:
        mock.post(url, text=json.dumps(create_response))
        obj = fl33t_client.Device(
            device_id=device_id,
            name=name,
            fleet_id=fleet_id
        )

        response = obj.create()
        assert isinstance(response, Device)
        assert response.device_id == device_id
        assert response.session_token == session_token


def test_delete(fl33t_client):
    device_id = 'asdf'
    fleet_id = 'fdsa'

    get_response = {
        "device": {
            "build_id": None,
            "checkin_tstamp": "2018-03-31T22:31:08.836406Z",
            "device_id": device_id,
            "name": "My Device",
            "fleet_id": fleet_id,
            "session_token": "poiuytrewq"
        }
    }

    url = '{}/team/{}/device/{}'.format(
            fl33t_client.base_uri, fl33t_client.team_id, device_id)

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(get_response))
        mock.delete(url, [{'status_code': 204}])

        obj = fl33t_client.get_device(device_id)
        assert obj.delete() is True


def test_list(fl33t_client):
    list_response = {
        "device_count": 2,
        "devices": [
            {
                "build_id": None,
                "checkin_tstamp": "2018-05-30T22:31:08.836406Z",
                "device_id": "asdf",
                "fleet_id": "fdsa",
                "name": "My Primary Device",
                "session_token": "poiuytrewq"
            },
            {
                "build_id": "erty",
                "checkin_tstamp": "2018-04-30T22:31:08.836406Z",
                "device_id": "qwer",
                "fleet_id": "fdsa",
                "name": "My Other Device",
                "session_token": "lkjhgfdsa"
            },
        ]
    }

    url = '{}/team/{}/devices'.format(
            fl33t_client.base_uri, fl33t_client.team_id)

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(list_response))
        objs = []
        for obj in fl33t_client.list_devices():
            assert isinstance(obj, Device)
            objs.append(obj)

        assert len(objs) == 2


def test_update(fl33t_client):

    device_id = "asdf"
    train_id = "fdsa"
    new_name = "My New Devices"

    update_response = {
        "device": {
            "build_id": None,
            "device_id": device_id,
            "name": new_name,
            "size": 5,
            "train_id": train_id,
            "unreleased": True
        }
    }

    get_response = copy.copy(update_response)
    get_response['device']['name'] = "My Devices"
    get_response['device']['unreleased'] = False

    url = '{}/team/{}/device/{}'.format(
            fl33t_client.base_uri, fl33t_client.team_id, device_id)

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(get_response))
        mock.put(url, text=json.dumps(update_response), status_code=204)

        obj = fl33t_client.get_device(device_id)
        obj.name = new_name
        obj.unreleased = True

        response = obj.update()

        assert isinstance(response, Device)
        assert response.name == new_name
        assert response.unreleased is True


def test_upgrade_available(fl33t_client):
    device_id = 'asdf'
    fleet_id = 'fdsa'
    train_id = 'zxcv'

    get_response = {
        "device": {
            "build_id": None,
            "checkin_tstamp": "2018-03-31T22:31:08.836406Z",
            "device_id": device_id,
            "name": "My Device",
            "fleet_id": fleet_id,
            "session_token": "poiuytrewq"
        }
    }

    upgrade_response = {
        "build": {
            "build_id": "mnbv",
            "download_url": "https://builds.example.com/some/build/path",
            "filename": "build.tgz",
            "md5sum": "14758f1afd44c09b7992073ccf00b43d",
            "released": True,
            "size": 42768345,
            "status": "available",
            "train_id": train_id,
            "upload_tstamp": "2018-05-30T22:31:08.836406Z",
            "upload_url": None,
            "version": "0.2"
        }
    }

    url = '{}/team/{}/device/{}'.format(
            fl33t_client.base_uri, fl33t_client.team_id, device_id)

    build_url = '{}/build'.format(url)

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(get_response))
        mock.get(build_url, text=json.dumps(upgrade_response))

        obj = fl33t_client.get_device(device_id)
        assert isinstance(obj, Device)

        build = obj.upgrade_available()
        assert isinstance(build, Build)
        assert build.train_id == train_id
