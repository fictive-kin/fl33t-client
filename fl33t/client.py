"""
Fl33t Client

The main client class that is used to interact with Fl33t
"""

import logging
import random
import string

import requests

from fl33t.exceptions import (
    InvalidBuildIdError,
    InvalidDeviceIdError,
    InvalidFleetIdError,
    InvalidSessionIdError,
    InvalidTrainIdError,
    UnprivilegedToken,
    Fl33tApiException
)

from fl33t.models.base import BaseModel
from fl33t.models import (
    Build,
    Device,
    Fleet,
    Train,
    Session
)

LOGGER = logging.getLogger(__name__)
API_HOST = 'https://api.fl33t.com'


class Fl33tClient:  # pylint: disable=too-many-public-methods
    """
    Handle all Fl33t-related interactions.

    Fl33t is used for managing firmware build trains.

    REST API docs: https://www.fl33t.com/docs/rest
    """

    # pylint: disable=too-many-arguments
    def __init__(self,
                 team_id,
                 session_token,
                 base_uri=None,
                 generated_id_length=None,
                 default_query_limit=None):
        """Establish basic service object."""

        self.team_id = team_id

        if not session_token:
            raise ValueError('session_token MUST be set!')

        self.token = session_token

        self.base_uri = base_uri if base_uri else API_HOST

        if generated_id_length:
            self.generated_id_length = int(generated_id_length)
            if self.generated_id_length < 1:
                self.generated_id_length = 6
        else:
            self.generated_id_length = 6

        if default_query_limit:
            self.default_query_limit = int(default_query_limit)
            if self.default_query_limit < 1:
                self.default_query_limit = 25
        else:
            self.default_query_limit = 25

    def Build(self, **kwargs):  # pylint: disable=invalid-name
        """Return a client connected Build"""
        return Build(client=self, **kwargs)

    def Device(self, **kwargs):  # pylint: disable=invalid-name
        """Return a client connected Device"""
        return Device(client=self, **kwargs)

    def Fleet(self, **kwargs):  # pylint: disable=invalid-name
        """Return a client connected Fleet"""
        return Fleet(client=self, **kwargs)

    def Train(self, **kwargs):  # pylint: disable=invalid-name
        """Return a client connected Train"""
        return Train(client=self, **kwargs)

    def Session(self, **kwargs):  # pylint: disable=invalid-name
        """Return a client connected Session"""
        return Session(client=self, **kwargs)

    def base_team_url(self):
        """Returns the base team URL for this client"""
        return '/'.join((self.base_uri, 'team/{}'.format(self.team_id)))

    def _build_offset_limit(self, offset=None, limit=None):
        """Get the offset/limit query params allowing defaults"""
        if not offset or int(offset) < 1:
            offset = 0

        if not limit or int(limit) < 1:
            limit = self.default_query_limit

        return {
            'offset': offset,
            'limit': limit
        }

    def generate_id_string(self):
        """Generate random string for use in Fl33t ids."""
        return ''.join(random.SystemRandom().choice(
            string.ascii_lowercase + string.digits) for _ in range(
                self.generated_id_length))

    def get(self, url, **kwargs):
        """Send a GET request"""
        return self.request('GET', url, **kwargs)

    def post(self, url, **kwargs):
        """Send a POST request"""
        return self.request('POST', url, **kwargs)

    def put(self, url, **kwargs):
        """Send a PUT request"""
        return self.request('PUT', url, **kwargs)

    def delete(self, url, **kwargs):
        """Send a DELETE request"""
        return self.request('DELETE', url, **kwargs)

    def request(self, method, url, **kwargs):
        """
        Wrapper for `requests` methods to include the bearer token
        If you need to make a call without the bearer token, make it
        directly against `requests`
        """

        headers = kwargs.get('headers') if kwargs.get('headers') else {}
        if 'Authorization' not in headers:
            headers['Authorization'] = 'Bearer {}'.format(self.token)
        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'
        if 'Accept' not in headers:
            headers['Accept'] = 'application/json'
        kwargs['headers'] = headers

        data = kwargs.pop('data', None)
        if data and isinstance(data, BaseModel):
            data = data.to_json()

        params = kwargs.pop('params', None)

        LOGGER.debug('Sending {} request with params: {}'.format(
            method, params))
        LOGGER.debug('Sending {} request with payload: {}'.format(
            method, data))
        method = getattr(requests, method.lower())
        try:
            result = method(url, params=params, data=data, **kwargs)
            result.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            LOGGER.exception(exc)

        if not result:
            return False

        if result.status_code == 403:
            raise UnprivilegedToken(url)

        if result.status_code >= 500:
            raise Fl33tApiException(url, result.status_code, result.text)

        return result

    def list_sessions(self, offset=None, limit=None):
        """
        List API Sessions
        """
        url = "/".join((self.base_team_url(), 'sessions'))
        params = self._build_offset_limit(offset=offset, limit=limit)

        result = self.get(url, params=params)

        for item in result.json()['sessions']:
            yield Session(client=self, **item)

    def get_own_session(self):
        """
        Return information about the current token
        """

        return self.get_session(self.token)

    def get_session(self, session_token):
        """
        Return information about a specific session_token
        """

        url = "/".join((self.base_team_url(), 'session/{}'.format(
            session_token)))

        result = self.get(url)
        if result:
            if result.status_code == 400:
                raise InvalidSessionIdError()

            if 'session' in result.json():
                session = result.json()['session']
                return Session(client=self, **session)

        LOGGER.exception('Could not retrieve session.')
        return False

    def get_fleet(self, fleet_id):
        """
        Return information about a specific fleet
        """

        url = "/".join((self.base_team_url(), 'fleet/{}'.format(fleet_id)))

        result = self.get(url)
        if result:
            if result.status_code == 400:
                raise InvalidFleetIdError(fleet_id)

            if 'fleet' in result.json():
                fleet = result.json()['fleet']
                return Fleet(client=self, **fleet)

        LOGGER.exception('Could not retrieve fleet: {}'.format(fleet_id))
        return False

    def get_build(self, train_id, build_id):
        """
        Return information about a specific build
        """

        url = "/".join((self.base_team_url(), 'train/{}/build/{}'.format(
            train_id, build_id)))

        result = self.get(url)
        if result:
            if result.status_code == 404:
                raise InvalidBuildIdError(build_id)

            if 'build' in result.json():
                build = result.json()['build']
                return Build(client=self, **build)

        LOGGER.exception(
            'Could not retrieve build: {} from train {}'.format(
                build_id, train_id))
        return False

    def get_train(self, train_id):
        """
        Return information about a specific train
        """

        url = "/".join((self.base_team_url(), 'train/{}'.format(
            train_id)))

        result = self.get(url)
        if result:
            if result.status_code == 400:
                raise InvalidTrainIdError(train_id)

            if 'train' in result.json():
                train = result.json()['train']
                return Train(client=self, **train)

        LOGGER.exception('Could not retrieve train: {}'.format(train_id))
        return False

    def get_device(self, device_id):
        """
        Get a device by ID from Fleet.
        """

        url = "/".join((self.base_team_url(), 'device/{}'.format(
            device_id)))

        result = self.get(url)
        if result:
            if result.status_code == 400:
                raise InvalidDeviceIdError(device_id)

            if 'device' in result.json():
                device = result.json()['device']
                return Device(client=self, **device)

        LOGGER.exception('Could not retrieve device: {}'.format(device_id))
        return False

    def has_upgrade_available(self, device_id, currently_installed_id=None):
        """
        Does this device have pending firmware updates?

        If ``currently_installed_id`` is specified, the value will be passed as
        a query argument to the fl33t endpoint.
        """

        url = '/'.join((self.base_team_url(), 'device/{}/build'.format(
            device_id)))

        params = None
        if currently_installed_id:
            params = {
                'installed_build_id': currently_installed_id
            }

        result = self.get(url, params=params)
        if result:
            # No update available.
            if result.status_code == 204:
                return False

            if 'build' in result.json():
                build = result.json()['build']
                return self.Build(**build)

        return False

    def list_fleets(self, train_id=None, offset=None, limit=None):
        """Get all fleets from fl33t."""

        url = "/".join((self.base_team_url(), 'fleets'))
        params = self._build_offset_limit(offset=offset, limit=limit)

        if train_id:
            params['train_id'] = train_id

        result = self.get(url, params=params)
        if not result or 'fleets' not in result.json():
            LOGGER.exception('Could not fetch fleets')
            return

        for item in result.json()['fleets']:
            yield Fleet(client=self, **item)

    def list_trains(self, offset=None, limit=None):
        """Get all trains from fl33t."""

        url = "/".join((self.base_team_url(), 'trains'))
        params = self._build_offset_limit(offset=offset, limit=limit)

        result = self.get(url, params=params)
        if not result or 'trains' not in result.json():
            LOGGER.exception('Could not fetch trains')
            return

        for item in result.json()['trains']:
            yield Train(client=self, **item)

    def list_devices(self, fleet_id=None, offset=None, limit=None):
        """Get all devices from fl33t."""

        url = "/".join((self.base_team_url(), 'devices'))
        params = self._build_offset_limit(offset=offset, limit=limit)
        if fleet_id:
            params['fleet_id'] = fleet_id

        result = self.get(url, params=params)
        if not result or 'devices' not in result.json():
            LOGGER.exception('Could not fetch devices')
            return

        for item in result.json()['devices']:
            yield Device(client=self, **item)

    def list_builds(self, train_id, version=None, offset=None, limit=None):
        """Get all builds from fl33t, by train id."""

        url = "/".join((self.base_team_url(), 'train/{}/builds'.format(
            train_id)))
        params = self._build_offset_limit(offset=offset, limit=limit)
        if version:
            params['version'] = version

        result = self.get(url, params=params)
        if not result or 'builds' not in result.json():
            LOGGER.exception('Could not fetch builds for train: {}'.format(
                train_id))
            return

        for item in result.json()['builds']:
            yield Build(client=self, **item)
