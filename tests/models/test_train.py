
import copy
import datetime
import json
import requests_mock

from fl33t.models import Train


def test_create(fl33t_client):
    train_id = 'fdsa'
    name = "My Train's Name"

    create_response = {
        "train": {
            "train_id": train_id,
            "name": name,
            "upload_tstamp": "2018-05-30T22:31:08.836406Z"
        }
    }

    url = '/'.join((
        fl33t_client.base_team_url(),
        'train'
    ))

    with requests_mock.Mocker() as mock:
        mock.post(url, text=json.dumps(create_response))
        obj = fl33t_client.Train(
            name=name
        )

        response = obj.create()
        assert isinstance(response, Train)
        assert response.train_id == train_id


def test_delete(fl33t_client):
    train_id = 'asdf'

    get_response = {
        "train": {
            "train_id": train_id,
            "name": "My train's name",
            "upload_tstamp": "2018-05-30T22:31:08.836406Z"
        }
    }

    url = '/'.join((
        fl33t_client.base_team_url(),
        'train',
        train_id
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(get_response))
        mock.delete(url, [{'status_code': 204}])

        obj = fl33t_client.get_train(train_id)
        assert obj.delete() is True


def test_list(fl33t_client):
    list_response = {
        "train_count": 2,
        "trains": [
            {
                "train_id": "asdf",
                "name": "My Train's Name",
                "upload_tstamp": "2018-05-30T22:31:08.836406Z"
            },
            {
                "train_id": "fdsa",
                "name": "My Other Train's Name",
                "upload_tstamp": "2018-05-30T22:31:08.836406Z"
            },
        ]
    }

    url = '/'.join((
        fl33t_client.base_team_url(),
        'trains'
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(list_response))
        objs = []
        for obj in fl33t_client.list_trains():
            assert isinstance(obj, Train)
            assert isinstance(obj.upload_tstamp, datetime.datetime)
            objs.append(obj)

        assert len(objs) == 2


def test_update(fl33t_client):

    train_id = 'fdsa'
    new_name = "My Train's New Name"

    update_response = {
        "train": {
            "train_id": train_id,
            "name": new_name,
            "upload_tstamp": "2018-05-30T22:31:08.836406Z"
        }
    }

    get_response = copy.copy(update_response)
    get_response['train']['name'] = "My Train's Old Name"

    url = '/'.join((
        fl33t_client.base_team_url(),
        'train',
        train_id
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(get_response))
        mock.put(url, text=json.dumps(update_response), status_code=204)

        obj = fl33t_client.get_train(train_id)
        obj.name = new_name

        response = obj.update()

        assert isinstance(response, Train)
        assert response.train_id == train_id
        assert response.name == new_name
