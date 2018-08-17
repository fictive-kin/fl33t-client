
import copy
import datetime
import json
import requests_mock

from fl33t.models import Build


def test_create(fl33t_client):
    build_id = 'zxcv'
    train_id = 'fdsa'
    version = '0.1.4'
    upload_url = "https://builds.example.com/some/build/path"

    create_response = {
        "build": {
            "build_id": build_id,
            "download_url": None,
            "filename": None,
            "md5sum": "14758f1afd44c09b7992073ccf00b43d",
            "released": False,
            "size": None,
            "status": "created",
            "train_id": train_id,
            "upload_tstamp": None,
            "upload_url": upload_url,
            "version": version
        }
    }

    url = '/'.join((
        fl33t_client.base_team_url(),
        'train',
        train_id,
        'build'
    ))

    with requests_mock.Mocker() as mock:
        mock.post(url, text=json.dumps(create_response))
        mock.put(upload_url, [{'status_code': 200}])
        obj = fl33t_client.Build(
            train_id=train_id,
            version=version,
            filename=__file__
        )

        response = obj.create()
        assert isinstance(response, Build)
        assert response.build_id == build_id


def test_delete(fl33t_client):
    train_id = 'asdf'
    build_id = 'fdsa'

    get_response = {
        "build": {
            "build_id": build_id,
            "download_url": "https://builds.example.com/some/build/path",
            "filename": "build.tgz",
            "md5sum": "14758f1afd44c09b7992073ccf00b43d",
            "released": False,
            "size": 42768345,
            "status": "available",
            "train_id": train_id,
            "upload_tstamp": "2018-05-30T22:31:08.836406Z",
            "upload_url": None,
            "version": "0.1"
        }
    }

    url = '/'.join((
        fl33t_client.base_team_url(),
        'train',
        train_id,
        'build',
        build_id
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(get_response))
        mock.delete(url, [{'status_code': 204}])

        obj = fl33t_client.get_build(train_id, build_id)
        assert obj.delete() is True


def test_list(fl33t_client):
    train_id = 'fdsa'

    list_response = {
        "build_count": 2,
        "builds": [
            {
                "build_id": "asdf",
                "download_url": "https://builds.example.com/path/to/download",
                "filename": "build.tar",
                "md5sum": "14758f1afd44c09b7992073ccf00b43d",
                "released": False,
                "size": 1234,
                "status": "available",
                "train_id": train_id,
                "upload_tstamp": "2018-05-30T22:31:08.836406Z",
                "upload_url": None,
                "version": "0.1"
            },
            {
                "build_id": "poiu",
                "download_url":
                    "https://builds.example.com/path/to/otherdownload",
                "filename": "build.tar",
                "md5sum": "14758f1afd23c09b7992073ccf00b43d",
                "released": True,
                "size": 4321,
                "status": "available",
                "train_id": train_id,
                "upload_tstamp": "2018-05-30T22:31:08.836406Z",
                "upload_url": None,
                "version": "0.2"
            },
        ]
    }

    url = '/'.join((
        fl33t_client.base_team_url(),
        'train',
        train_id,
        'builds'
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(list_response))
        objs = []
        for obj in fl33t_client.list_builds(train_id):
            assert isinstance(obj, Build)
            assert obj.train_id == train_id
            assert isinstance(obj.upload_tstamp, datetime.datetime)
            objs.append(obj)

        assert len(objs) == 2


def test_update(fl33t_client):

    build_id = 'zxcv'
    train_id = 'fdsa'

    update_response = {
        "build": {
            "build_id": build_id,
            "download_url": "https://build.example.com/some/build/path",
            "filename": "build.tar",
            "md5sum": "14758f1afd44c09b7992073ccf00b43d",
            "released": True,
            "size": 4321,
            "status": "available",
            "train_id": train_id,
            "upload_tstamp": "2018-05-30T22:31:08.836406Z",
            "upload_url": None,
            "version": "0.3"
        }
    }

    get_response = copy.copy(update_response)
    get_response['build']['released'] = False

    url = '/'.join((
        fl33t_client.base_team_url(),
        'train',
        train_id,
        'build',
        build_id
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(get_response))
        mock.put(url, text=json.dumps(update_response), status_code=204)

        obj = fl33t_client.get_build(train_id, build_id)
        obj.released = True

        response = obj.update()

        assert isinstance(response, Build)
        assert response.build_id == build_id
        assert response.released is True
