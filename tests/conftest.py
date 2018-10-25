
import pytest

from fl33t import Fl33tClient


@pytest.yield_fixture
def api_host():
    return 'https://api.example.com'


@pytest.yield_fixture
def team_id():
    return 'meli'


@pytest.yield_fixture
def session_token():
    return 'asdfasdfasdfasdfasdfsadfasdfasdf'


@pytest.yield_fixture
def fleet_id():
    return "fake-fleet-id"


@pytest.yield_fixture
def train_id():
    return "fake-train-id"


@pytest.yield_fixture
def build_id():
    return "fake-build-id"


@pytest.yield_fixture
def device_id():
    return "fake-device-id"


@pytest.yield_fixture
def fl33t_client(team_id, session_token, api_host):
    return Fl33tClient(
        team_id,
        session_token,
        base_uri=api_host
    )


@pytest.yield_fixture
def device_get_response(device_id, fleet_id, build_id):
    return {
        "device": {
            "build_id": build_id,
            "checkin_tstamp": "2018-03-31T22:31:08.836406Z",
            "device_id": device_id,
            "name": "My Device",
            "fleet_id": fleet_id,
            "session_token": "poiuytrewq"
        }
    }


@pytest.yield_fixture
def fleet_get_response(fleet_id, train_id, build_id):
    return {
        "fleet": {
            "build_id": build_id,
            "fleet_id": fleet_id,
            "name": "My Devices",
            "size": 5,
            "train_id": train_id,
            "unreleased": True
        }
    }


@pytest.yield_fixture
def train_get_response(train_id):
    return {
        "train": {
            "train_id": train_id,
            "name": "Long Train Running",
            "upload_tstamp": "2018-05-30T22:31:08.836406Z"
        }
    }


@pytest.yield_fixture
def build_get_response(train_id, build_id):
    return {
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
