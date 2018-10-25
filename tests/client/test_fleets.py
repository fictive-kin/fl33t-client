
import json
import pytest
import requests_mock

from fl33t.exceptions import InvalidFleetIdError
from fl33t.models import Fleet


def test_get_fleet(fl33t_client):
    train_id = 'bvcx'
    fleet_id = 'mnbv'

    fleet_response = {
        'fleet': {
            'build_id': None,
            'fleet_id': fleet_id,
            'name': 'Fake Fleet',
            'size': 5,
            'train_id': train_id,
            'unreleased': False
        }
    }

    url = '/'.join((
        fl33t_client.base_team_url,
        'fleet',
        fleet_id
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(fleet_response))

        obj = fl33t_client.get_fleet(fleet_id)

        assert isinstance(obj, Fleet)
        assert obj.fleet_id == fleet_id


def test_fail_get_fleet_invalid_id(fl33t_client):
    fleet_id = 'fdsa'

    url = '/'.join((
        fl33t_client.base_team_url,
        'fleet',
        fleet_id
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, [
            {'status_code': 400, 'text': 'Invalid fleet ID'},
            {'status_code': 404, 'text': 'Page not found'}
        ])

        with pytest.raises(InvalidFleetIdError):
            fl33t_client.get_fleet(fleet_id)
            fl33t_client.get_fleet(fleet_id)
