
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
def fl33t_client(team_id, api_host):
    return Fl33tClient(
        team_id,
        session_token,
        base_uri=api_host
    )
