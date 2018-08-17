
import json
import pytest
import requests_mock

from fl33t.exceptions import InvalidTrainIdError
from fl33t.models import Train


def test_get_train(fl33t_client):
    train_id = 'asdf'

    train_response = {
        'train': {
            'train_id': train_id,
            'upload_tstamp': '2018-03-31T22:31:08.836406Z',
            'name': 'Fake Train'
        }
    }

    url = '/'.join((
        fl33t_client.base_team_url(),
        'train',
        train_id
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, text=json.dumps(train_response))

        obj = fl33t_client.get_train(train_id)

        assert isinstance(obj, Train)
        assert obj.name == 'Fake Train'


def test_fail_get_train_invalid_id(fl33t_client):
    train_id = 'asdf'

    url = '/'.join((
        fl33t_client.base_team_url(),
        'train',
        train_id
    ))

    with requests_mock.Mocker() as mock:
        mock.get(url, [
            {'status_code': 400, 'text': 'Invalid train ID'},
            {'status_code': 404, 'text': 'Page not found'}
        ])

        with pytest.raises(InvalidTrainIdError):
            obj = fl33t_client.get_train(train_id)
            obj = fl33t_client.get_train(train_id)
