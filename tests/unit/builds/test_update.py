
import copy
import json
import pytest
import requests_mock

from fl33t.models import Build

def test_update_build(fl33t_client):

    build_id = 'zxcv'
    train_id = 'fdsa'

    update_build_response = {
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

    get_build_response = copy.copy(update_build_response)
    get_build_response['build']['released'] = False

    url = '{}/team/{}/train/{}/build/{}'.format(
            fl33t_client.base_uri, fl33t_client.team_id, train_id, build_id)

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(get_build_response))
        mock.put(url, text=json.dumps(update_build_response), status_code=204)

        build = fl33t_client.get_build(train_id, build_id)
        build.released = True

        response = build.update()

        assert isinstance(response, Build)
        assert response.build_id == build_id
        assert response.released == True
