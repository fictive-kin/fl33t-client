
import json
import pytest
import requests_mock

from fl33t.models import Build

def test_list_builds(fl33t_client):
    train_id = 'fdsa'

    list_builds_response = {
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
                "download_url": "https://builds.example.com/path/to/otherdownload",
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

    url = '{}/team/{}/train/{}/builds'.format(
            fl33t_client.base_uri, fl33t_client.team_id, train_id)

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(list_builds_response))
        builds = []
        for build in fl33t_client.list_builds(train_id):
            assert isinstance(build, Build)
            assert build.train_id == train_id
            builds.append(build)

        assert len(builds) == 2
