
import json
import pytest
import requests_mock

from fl33t.exceptions import InvalidDeviceIdError
from fl33t.models import Device


def test_get_device(fl33t_client):
    device_id = 'mnbv'
    fleet_id = 'vbnm'

    device_response = {
        'device': {
            'build_id': None,
            'checkin_tstamp': '2018-03-31T22:31:08.836406Z',
            'device_id': device_id,
            'name': 'Fake Device',
            'fleet_id': fleet_id,
            'session_token': 'poiuytre'
        }
    }

    url = '/'.join((
        fl33t_client.base_team_url(),
        'device',
        device_id
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(device_response))

        obj = fl33t_client.get_device(device_id)

        assert isinstance(obj, Device)
        assert obj.fleet_id == fleet_id


def test_fail_get_device_invalid_id(fl33t_client):
    device_id = 'asdffdsa'

    url = '/'.join((
        fl33t_client.base_team_url(),
        'device',
        device_id
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, [
            {'status_code': 400, 'text': 'Invalid device ID'},
            {'status_code': 404, 'text': 'Page not found'}
        ])

        with pytest.raises(InvalidDeviceIdError):
            obj = fl33t_client.get_device(device_id)
            obj = fl33t_client.get_device(device_id)
