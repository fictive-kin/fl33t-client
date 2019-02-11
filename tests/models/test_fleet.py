
import copy
import json
import requests_mock

from fl33t.models import Fleet, Train, Build


def test_create(fl33t_client, fleet_id, train_id):
    name = 'My Devices'
    size = 5

    create_response = {
        "fleet": {
            "build_id": None,
            "fleet_id": fleet_id,
            "name": name,
            "size": size,
            "train_id": train_id,
            "unreleased": True
        }
    }

    url = '/'.join((
        fl33t_client.base_team_url,
        'fleet'
    ))

    with requests_mock.Mocker() as mock:
        mock.post(url, text=json.dumps(create_response))
        obj = fl33t_client.Fleet(
            name=name,
            unreleased=True,
            train_id=train_id
        )

        response = obj.create()
        assert isinstance(response, Fleet)
        assert response.id == fleet_id
        assert str(response) == ('Fleet {}: {} (Train: {}, Status: {}, '
            'Size: {})'.format(
                fleet_id,
                name,
                train_id,
                'Unreleased',
                size
            )
        )

        assert repr(response) == ('<Fleet id={} name={} train_id={} '
            'unreleased={} size={}>'.format(
                fleet_id,
                name,
                train_id,
                True,
                size
            )
        )


def test_delete(fl33t_client, fleet_id, train_id, fleet_get_response):

    url = '/'.join((
        fl33t_client.base_team_url,
        'fleet',
        fleet_id
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(fleet_get_response))
        mock.delete(url, [{'status_code': 204}])

        obj = fl33t_client.get_fleet(fleet_id)
        assert obj.delete() is True


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

    url = '/'.join((
        fl33t_client.base_team_url,
        'fleets'
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(list_response))
        objs = []
        for obj in fl33t_client.list_fleets():
            assert isinstance(obj, Fleet)
            objs.append(obj)

        assert len(objs) == 2


def test_update(fl33t_client, fleet_id, train_id, fleet_get_response):

    new_name = "My New Devices"

    update_response = copy.copy(fleet_get_response)
    update_response['fleet']['name'] = new_name
    update_response['fleet']['unreleased'] = True

    url = '/'.join((
        fl33t_client.base_team_url,
        'fleet',
        fleet_id
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(fleet_get_response))
        mock.put(url, text=json.dumps(update_response), status_code=204)

        obj = fl33t_client.get_fleet(fleet_id)
        obj.name = new_name
        obj.unreleased = True

        response = obj.update()

        assert isinstance(response, Fleet)
        assert response.name == new_name
        assert response.unreleased is True


def test_parent_train(fl33t_client,
                      fleet_id,
                      train_id,
                      fleet_get_response,
                      train_get_response):

    url = '/'.join((
        fl33t_client.base_team_url,
        'fleet',
        fleet_id
    ))

    train_url = '/'.join((
        fl33t_client.base_team_url,
        'train',
        train_id
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(fleet_get_response))
        mock.get(train_url, text=json.dumps(train_get_response))

        obj = fl33t_client.get_fleet(fleet_id)

        assert isinstance(obj.train, Train)
        assert obj.train.train_id == train_id


def test_parent_build(fl33t_client,
                      fleet_id,
                      build_id,
                      fleet_get_response,
                      build_get_response):

    url = '/'.join((
        fl33t_client.base_team_url,
        'fleet',
        fleet_id
    ))

    build_url = '/'.join((
        fl33t_client.base_team_url,
        'build',
        build_id
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(fleet_get_response))
        mock.get(build_url, text=json.dumps(build_get_response))

        obj = fl33t_client.get_fleet(fleet_id)

        assert isinstance(obj.build, Build)
        assert obj.build.build_id == build_id
