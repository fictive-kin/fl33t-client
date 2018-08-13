
import base64
import json
import logging
import os
import random
import requests
import string

from fl33t.exceptions import(
    DuplicateDeviceIdError,
    InvalidDeviceIdError,
    InvalidSessionIdError,
    InvalidBuildIdError,
    InvalidFleetIdError,
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

from fl33t.utils import md5

logger = logging.getLogger(__name__)

API_HOST = 'https://api.fl33t.com'

class Fl33tClient:
    """
    Handle all Fl33t-related interactions.

    Fl33t is used for managing firmware build trains.

    REST API docs: https://www.fl33t.com/docs/rest
    """

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


    def Build(self, **kwargs):
        return Build(client=self, **kwargs)

    def Device(self, **kwargs):
        return Device(client=self, **kwargs)

    def Fleet(self, **kwargs):
        return Fleet(client=self, **kwargs)

    def Train(self, **kwargs):
        return Train(client=self, **kwargs)

    def Session(self, **kwargs):
        return Session(client=self, **kwargs)


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


    def _generate_id_string(self):
        """Generate random string for use in Fl33t ids."""
        return ''.join(random.SystemRandom().choice(
            string.ascii_lowercase + string.digits) for _ in range(
                self.generated_id_length))


    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)


    def post(self, url, **kwargs):
        return self.request('POST', url, **kwargs)


    def put(self, url, **kwargs):
        return self.request('PUT', url, **kwargs)


    def delete(self, url, **kwargs):
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

        logger.debug('Sending {} request with params: {}'.format(
            method, params))
        logger.debug('Sending {} request with payload: {}'.format(
            method, data))
        method = getattr(requests, method.lower())
        try:
            result = method(url, params=params, data=data, **kwargs)
            result.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.exception(e)
            pass

        if not result:
            return False

        if result.status_code == 403:
            raise UnprivilegedToken(url)

        if result.status_code >= 500:
            raise Fl33tApiException(result.status_code, result.text)

        return result


    def list_sessions(self, offset=None, limit=None):
        """
        List API Sessions
        """
        url = "/".join((self.base_uri, 'team/{}/sessions'.format(
            self.team_id)))
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

        url = "/".join((self.base_uri, 'team/{}/session/{}'.format(
            self.team_id, session_token)))

        result = self.get(url)
        if result:
            if result.status_code == 400:
                raise InvalidSessionIdError()

            if 'session' in result.json():
                session = result.json()['session']
                return Session(client=self, **session)

        logger.exception('Could not retrieve session.')
        return False


    def get_fleet(self, fleet_id):
        """
        Return information about a specific fleet
        """

        url = "/".join((self.base_uri, 'team/{}/fleet/{}'.format(
            self.team_id, fleet_id)))

        result = self.get(url)
        if result:
            if 'fleet' in result.json():
                fleet = result.json()['fleet']
                return Fleet(client=self, **fleet)

        logger.exception(
            'Could not retrieve fleet: {} from train {}'.format(fleet_id))
        return False


    def get_build(self, build_id, train_id):
        """
        Return information about a specific build
        """

        url = "/".join((self.base_uri, 'team/{}/train/{}/build/{}'.format(
            self.team_id, train_id, build_id)))

        result = self.get(url)
        if result:
            if result.status_code == 404:
                raise InvalidBuildIdError()

            if 'build' in result.json():
                build = result.json()['build']
                return Build(client=self, **build)

        logger.exception(
            'Could not retrieve build: {} from train {}'.format(
                build_id, train_id))
        return False


    def get_train(self, train_id):
        """
        Return information about a specific train
        """

        url = "/".join((self.base_uri, 'team/{}/train/{}'.format(
            self.team_id, train_id)))

        result = self.get(url)
        if result:
            if 'train' in result.json():
                train = result.json()['train']
                return Train(client=self, **train)

        logger.exception('Could not retrieve train: {}'.format(train_id))
        return False


    def get_device(self, device_id):
        """
        Get a device by ID from Fleet.
        """

        url = "/".join((self.base_uri, 'team/{}/device/{}'.format(
            self.team_id, device_id)))

        result = self.get(url)
        if result:
            if result.status_code == 400:
                raise InvalidDeviceIdError()
            if 'device' in result.json():
                device = result.json()['device']
                return Device(client=self, **device)

        logger.exception('Could not retrieve device: {}'.format(device_id))
        return False


    def create_device_id(self, fleet_id, device_id=None, name=None):
        """
        Create a device ID in Fleet.

        If ``device_id`` is specified, used that as the ID If not specified, a
        random string will be used instead.
        """

        device_id = device_id or self._generate_id_string()

        url = "/".join((self.base_uri, 'team/{}/device'.format(self.team_id)))
        data = {
            'device': {
                'device_id': device_id,
                'name': name,
                'fleet_id': fleet_id
            }
        }

        result = self.post(url, data=data)
        if result:
            if result.status_code == 409:
                raise DuplicateDeviceIdError()
            if 'device' in result.json():
                device = result.json()['device']
                return Device(client=self, **device)

        logger.exception('Could not create device')
        return False


    def delete_device_id(self, device_id):
        """Delete a device by device ID in Fleet."""

        url = "/".join((self.base_uri, 'team/{}/device/{}'.format(
            self.team_id, device_id)))

        result = self.delete(url)
        if result:
            if result.status_code == 400:
                raise InvalidDeviceIdError()

            # Device has been deleted if 204.
            return result.status_code == 204

        logger.exception('Could not delete device')
        return False


    def has_firmware_update(self, device_id, currently_installed_id=None):
        """
        Does this device have pending firmware updates?

        If ``currently_installed_id`` is specified, the value will be passed as
        a query argument to the fl33t endpoint.
        """

        url = "/".join((self.base_uri, 'team/{}/device/{}/build'.format(
            self.team_id, device_id)))
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
                return Build(client=self, **build)

        logger.exception('Could not check for firmware updates')
        return False


    def list_fleets(self, train_id=None, offset=None, limit=None):
        """Get all fleets from fl33t."""

        url = "/".join((self.base_uri, 'team/{}/fleets'.format(self.team_id)))
        params = self._build_offset_limit(offset=offset, limit=limit)
        if train_id:
            params['train_id'] = train_id

        result = self.get(url, params=params)
        if not result or 'fleets' not in result.json():
            logger.exception('Could not fetch fleets')
            return False

        for item in result.json()['fleets']:
            yield Fleet(client=self, **item)


    def list_trains(self, offset=None, limit=None):
        """Get all trains from fl33t."""

        url = "/".join((self.base_uri, 'team/{}/trains'.format( self.team_id)))
        params = self._build_offset_limit(offset=offset, limit=limit)

        result = self.get(url, params=params)
        if not result or 'trains' not in result.json():
            logger.exception('Could not fetch trains')
            return False

        for item in result.json()['trains']:
            yield Train(client=self, **item)


    def list_devices(self, fleet_id=None, offset=None, limit=None):
        """Get all devices from fl33t."""

        url = "/".join((self.base_uri, 'team/{}/devices'.format(self.team_id)))
        params = self._build_offset_limit(offset=offset, limit=limit)
        if fleet_id:
            params['fleet_id'] = fleet_id

        result = self.get(url, params=params)
        if not result or 'devices' not in result.json():
            logger.exception('Could not fetch devices')
            return False

        for item in result.json()['devices']:
            yield Device(client=self, **item)


    def list_builds(self, train_id, version=None, offset=None, limit=None):
        """Get all builds from fl33t, by train id."""

        url = "/".join((self.base_uri, 'team/{}/train/{}/builds'.format(
            self.team_id, train_id)))
        params = self._build_offset_limit(offset=offset, limit=limit)
        if version:
            params['version'] = version

        result = self.get(url, params=params)
        if not result or 'builds' not in result.json():
            logger.exception('Could not fetch builds for train: {}'.format(train_id))
            return False

        for item in result.json()['builds']:
            yield Build(client=self, **item)


    def build_update(self, build):
        pass


    def build_delete(self, build):
        """Delete a build from a Fl33t train"""

        url = "/".join((self.base_uri, 'team/{}/train/{}/build/{}'.format(
            self.team_id, build.train_id, build.build_id)))

        result = self.delete(url)
        return result.status_code == 204


    def build_create(self, build):
        """Create a new build record in fl33t and upload the new build file"""

        url = "/".join((self.base_uri, 'team/{}/train/{}/build'.format(
            self.team_id, build.train_id)))

        data = {
            'build': build.to_json()
        }

        result = self.post(url, data=build)
        if not result or 'build' not in result.json():
            logger.exception(
                'Could not create build for: {}'.format(build.version))
            return False

        build_data = result.json()['build']
        for key in build_data.keys():
            setattr(build, key, build_data[key])

        if not build.upload_url:
            logger.exception(
                'Build creation worked, but no upload_url was'
                ' provided by fl33t for build: {}'.format(build.version))
            return build

        headers = {
            'Content-Type': 'application/octet-stream',
            'Content-Disposition': 'attachment; filename="{}"'.format(
                build.filename)
        }
        with open(build.fullpath, 'rb') as build_file:
            response = requests.put(
                build.upload_url,
                data=build_file.read(),
                headers=headers)

            if not response or response.status_code != 200:
                logger.exception(
                    'Failed to upload build file: {}'.format(build.version))
                return False

        return build
