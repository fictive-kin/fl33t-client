
import copy
import datetime
import json
import pytest
import requests_mock

from fl33t.exceptions import DuplicateDeviceIdError
from fl33t.models import Device, Build, Fleet


def test_create(fl33t_client, device_id, fleet_id):
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

    url = '/'.join((
        fl33t_client.base_team_url,
        'device',
    ))

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


def test_delete(fl33t_client, device_id, fleet_id, device_get_response):

    url = '/'.join((
        fl33t_client.base_team_url,
        'device',
        device_id
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(device_get_response))
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

    url = '/'.join((
        fl33t_client.base_team_url,
        'devices'
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(list_response))
        objs = []
        for obj in fl33t_client.list_devices():
            assert isinstance(obj, Device)
            assert isinstance(obj.checkin_tstamp, datetime.datetime)
            objs.append(obj)

        assert len(objs) == 2


def test_update(fl33t_client, device_id, fleet_id, device_get_response):

    new_name = "My New Device"

    update_response = {
        "device": {
            "build_id": None,
            "checkin_tstamp": "2018-05-30T22:31:08.836406Z",
            "device_id": device_id,
            "fleet_id": fleet_id,
            "name": new_name,
            "session_token": "poiuytrewq"
        }
    }

    update_response = copy.copy(device_get_response)
    update_response['device']['name'] = new_name

    url = '/'.join((
        fl33t_client.base_team_url,
        'device',
        device_id
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(device_get_response))
        mock.put(url, text=json.dumps(update_response), status_code=204)

        obj = fl33t_client.get_device(device_id)
        obj.name = new_name

        response = obj.update()

        assert isinstance(response, Device)
        assert response.name == new_name


def test_upgrade_available(fl33t_client,
                           device_id,
                           fleet_id,
                           train_id,
                           device_get_response):

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

    url = '/'.join((
        fl33t_client.base_team_url,
        'device',
        device_id
    ))

    build_url = '/'.join((url, 'build'))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(device_get_response))
        mock.get(build_url, text=json.dumps(upgrade_response))

        obj = fl33t_client.get_device(device_id)
        assert isinstance(obj, Device)

        build = obj.upgrade_available()
        assert isinstance(build, Build)
        assert build.train_id == train_id


def test_upgrade_not_available(fl33t_client,
                               device_id,
                               fleet_id,
                               device_get_response):

    url = '/'.join((
        fl33t_client.base_team_url,
        'device',
        device_id
    ))

    build_url = '/'.join((url, 'build'))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(device_get_response))
        mock.get(build_url, status_code=204)

        obj = fl33t_client.get_device(device_id)
        assert isinstance(obj, Device)

        build = obj.upgrade_available()
        assert isinstance(build, bool)
        assert build is False


def test_fail_duplicate_id(fl33t_client, device_id):

    device = fl33t_client.Device(device_id=device_id)

    url = '/'.join((
        fl33t_client.base_team_url,
        'device'
    ))

    with requests_mock.Mocker() as mock:
        mock.post(url, status_code=409)

        with pytest.raises(DuplicateDeviceIdError):
            device.create()


def test_parent_fleet(fl33t_client,
                      device_id,
                      fleet_id,
                      device_get_response,
                      fleet_get_response):

    url = '/'.join((
        fl33t_client.base_team_url,
        'device',
        device_id
    ))

    fleet_url = '/'.join((
        fl33t_client.base_team_url,
        'fleet',
        fleet_id
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(device_get_response))
        mock.get(fleet_url, text=json.dumps(fleet_get_response))

        obj = fl33t_client.get_device(device_id)

        assert isinstance(obj.fleet, Fleet)
        assert obj.fleet.fleet_id == fleet_id


def test_parent_build(fl33t_client,
                      device_id,
                      fleet_id,
                      train_id,
                      build_id,
                      device_get_response,
                      fleet_get_response,
                      build_get_response):

    url = '/'.join((
        fl33t_client.base_team_url,
        'device',
        device_id
    ))

    fleet_url = '/'.join((
        fl33t_client.base_team_url,
        'fleet',
        fleet_id
    ))

    build_url = '/'.join((
        fl33t_client.base_team_url,
        'train',
        train_id,
        'build',
        build_id
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(device_get_response))
        mock.get(fleet_url, text=json.dumps(fleet_get_response))
        mock.get(build_url, text=json.dumps(build_get_response))

        obj = fl33t_client.get_device(device_id)

        assert isinstance(obj.fleet.build, Build)
        assert obj.fleet.build.build_id == build_id
