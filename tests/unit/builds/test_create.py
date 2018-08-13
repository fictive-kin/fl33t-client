
import json
import pytest
import requests_mock

from fl33t.models import Build

def test_create_build(fl33t_client):
    build_id = 'zxcv'
    train_id = 'fdsa'
    version = '0.1.4'
    upload_url = "https://builds.example.com/some/build/path"

    create_build_response = {
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

    url = '{}/team/{}/train/{}/build'.format(
            fl33t_client.base_uri, fl33t_client.team_id, train_id)

    with requests_mock.Mocker() as mock:
        mock.post(url, text=json.dumps(create_build_response))
        mock.put(upload_url, [{'status_code': 200}])
        build = fl33t_client.Build(
            train_id=train_id,
            version=version,
            filename=__file__
        )

        response = build.create()
        assert isinstance(response, Build)
        assert response.build_id == build_id
