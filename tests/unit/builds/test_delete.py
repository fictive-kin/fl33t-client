
import json
import pytest
import requests_mock


def test_delete_build(fl33t_client):
    train_id = 'asdf'
    build_id = 'fdsa'

    get_build_response = {
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

    url = '{}/team/{}/train/{}/build/{}'.format(
            fl33t_client.base_uri, fl33t_client.team_id, train_id, build_id)

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(get_build_response))
        mock.delete(url, [{'status_code': 204}])

        build = fl33t_client.get_build(build_id, train_id)
        assert build.delete() == True
