
import copy
import json
import pytest
import requests_mock

from fl33t.models import Fleet

def test_create(fl33t_client):
    fleet_id = 'asdf'
    train_id = 'fdsa'
    name = 'My Devices'

    create_response = {
        "fleet": {
            "build_id": None,
            "fleet_id": fleet_id,
            "name": name,
            "size": 5,
            "train_id": train_id,
            "unreleased": True
        }
    }

    url = '{}/team/{}/fleet'.format(
            fl33t_client.base_uri, fl33t_client.team_id)

    with requests_mock.Mocker() as mock:
        mock.post(url, text=json.dumps(create_response))
        obj = fl33t_client.Fleet(
            name=name,
            unreleased=True,
            train_id=train_id
        )

        response = obj.create()
        assert isinstance(response, Fleet)
        assert response.fleet_id == fleet_id

def test_delete(fl33t_client):
    fleet_id = 'asdf'
    train_id = 'fdsa'

    get_response = {
        "fleet": {
            "build_id": None,
            "fleet_id": fleet_id,
            "name": "My Devices",
            "size": 5,
            "train_id": train_id,
            "unreleased": True
        }
    }

    url = '{}/team/{}/fleet/{}'.format(
            fl33t_client.base_uri, fl33t_client.team_id, fleet_id)

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(get_response))
        mock.delete(url, [{'status_code': 204}])

        obj = fl33t_client.get_fleet(fleet_id)
        assert obj.delete() == True

def test_list(fl33t_client):
    list_response = {
        "fleet_count": 2,
        "fleets": [
            {
                "build_id": None,
                "fleet_id": "asdf",
                "name": "My Devices",
                "size": 5,
                "train_id": "fdsa",
                "unreleased": True
            },
            {
                "build_id": "erty",
                "fleet_id": "qwer",
                "name": "My Other Devices",
                "size": 6,
                "train_id": "lkjh",
                "unreleased": False
            },
        ]
    }

    url = '{}/team/{}/fleets'.format(
            fl33t_client.base_uri, fl33t_client.team_id)

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(list_response))
        objs = []
        for obj in fl33t_client.list_fleets():
            assert isinstance(obj, Fleet)
            objs.append(obj)

        assert len(objs) == 2

def test_update(fl33t_client):

    fleet_id = "asdf"
    train_id = "fdsa"
    new_name = "My New Devices"

    update_response = {
        "fleet": {
            "build_id": None,
            "fleet_id": fleet_id,
            "name": new_name,
            "size": 5,
            "train_id": train_id,
            "unreleased": True
        }
    }

    get_response = copy.copy(update_response)
    get_response['fleet']['name'] = "My Devices"
    get_response['fleet']['unreleased'] = False

    url = '{}/team/{}/fleet/{}'.format(
            fl33t_client.base_uri, fl33t_client.team_id, fleet_id)

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(get_response))
        mock.put(url, text=json.dumps(update_response), status_code=204)

        obj = fl33t_client.get_fleet(fleet_id)
        obj.name = new_name
        obj.unreleased = True

        response = obj.update()

        assert isinstance(response, Fleet)
        assert response.name == new_name
        assert response.unreleased == True
