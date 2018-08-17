
import json
import pytest
import requests_mock

from fl33t.exceptions import InvalidBuildIdError
from fl33t.models import Build


def test_get_build(fl33t_client):
    build_id = 'mnbv'
    train_id = 'vbnm'

    build_response = {
        'build': {
            'build_id': build_id,
            'download_url': 'https://build.example.com/some/build/path',
            'filename': 'build.tar',
            'md5sum': '14758f1afd44c09b7992073ccf00b43d',
            'released': False,
            'size': 194503,
            'status': 'created',
            'train_id': train_id,
            'upload_tstamp': '2018-05-30T22:31:08.836406Z',
            'upload_url': None,
            'version': '5.4.1'
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
        mock.get(url, text=json.dumps(build_response))

        obj = fl33t_client.get_build(train_id, build_id)

        assert isinstance(obj, Build)
        assert obj.train_id == train_id


def test_fail_get_build_invalid_id(fl33t_client):
    build_id = 'asdf'
    train_id = 'fdsa'

    url = '/'.join((
        fl33t_client.base_team_url(),
        'train',
        train_id,
        'build',
        build_id
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, [
            {'status_code': 400, 'text': 'Invalid build ID'},
            {'status_code': 404, 'text': 'Page not found'}
        ])

        with pytest.raises(InvalidBuildIdError):
            obj = fl33t_client.get_build(train_id, build_id)
            obj = fl33t_client.get_build(train_id, build_id)
