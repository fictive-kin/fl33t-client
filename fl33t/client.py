"""
fl33t Client
============

The main client class that is used to interact with fl33t.
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

API_HOST = 'https://api.fl33t.com'

ENDPOINT_FAILED_MSG = 'The fl33t endpoint for {} returned an invalid response'


class Fl33tClient:  # pylint: disable=too-many-public-methods
    """
    Handles all fl33t-related interactions.

    fl33t is used for managing firmware build trains.

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

        self.logger = logging.getLogger(__name__)

    def Build(self, **kwargs):  # pylint: disable=invalid-name
        """
        Get a Build object pre-initialised with this API client

        Allowed parameters are documented on the
            :py:class:`fleet.models.Build` class

        :returns: :py:class:`fl33t.models.Build`
        """
        return Build(client=self, **kwargs)

    def Device(self, **kwargs):  # pylint: disable=invalid-name
        """
        Get a Device object pre-initialised with this API client

        Allowed parameters are documented on the
            :py:class:`fleet.models.Device` class

        :returns: :py:class:`fl33t.models.Device`
        """
        return Device(client=self, **kwargs)

    def Fleet(self, **kwargs):  # pylint: disable=invalid-name
        """
        Get a Fleet object pre-initialised with this API client

        Allowed parameters are documented on the
            :py:class:`fleet.models.Fleet` class

        :returns: :py:class:`fl33t.models.Fleet`
        """
        return Fleet(client=self, **kwargs)

    def Train(self, **kwargs):  # pylint: disable=invalid-name
        """
        Get a Train object pre-initialised with this API client

        Allowed parameters are documented on the
            :py:class:`fleet.models.Train` class

        :returns: :py:class:`fl33t.models.Train`
        """
        return Train(client=self, **kwargs)

    def Session(self, **kwargs):  # pylint: disable=invalid-name
        """
        Get a Session object pre-initialised with this API client

        Allowed parameters are documented on the
            :py:class:`fleet.models.Session` class

        :returns::py:class:`fl33t.models.Session`
        """
        return Session(client=self, **kwargs)

    def base_team_url(self):
        """
        Get the base team URL for this client

        :returns: str
        """
        return '/'.join((self.base_uri, 'team/{}'.format(self.team_id)))

    def _build_offset_limit(self, offset=None, limit=None):
        """
        Get the offset/limit query params allowing defaults

        :param offset: If provided, the starting offset for result sets.
            Defaults to 0
        :type offset: int or None
        :param limit: If provided, the number of records to return.
            Defaults to :py:attr:`default_query_limit`
        :type limit: int or None
        :returns: dict of parameters for use in a request
        """
        if not offset or int(offset) < 1:
            offset = 0

        if not limit or int(limit) < 1:
            limit = self.default_query_limit

        return {
            'offset': int(offset),
            'limit': int(limit)
        }

    def generate_id_string(self, length=None):
        """
        Generate random string for use in fl33t ids.

        :param length: The length of the returned random string. If not
            provided, it defaults to the value of
            :py:attr:`self.generated_id_length`
        :type length: int or None
        :returns: str
        """

        if not length:
            length = self.generated_id_length

        return ''.join(random.SystemRandom().choice(
            string.ascii_lowercase + string.digits) for _ in range(
                self.generated_id_length))

    def get(self, url, **kwargs):
        """
        Send an authenticated GET request to fl33t

        :param str url: The URL to request
        :param kwargs: Any keyword args that :py:class:`requests.get` accepts
        :returns: :py:class:`requests.Response`
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        """
        return self._request('GET', url, **kwargs)

    def post(self, url, **kwargs):
        """
        Send an authenticated POST request to fl33t

        :param str url: The URL to request
        :param kwargs: Any keyword args that :py:class:`requests.post` accepts
        :returns: :py:class:`requests.Response`
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        """
        return self._request('POST', url, **kwargs)

    def put(self, url, **kwargs):
        """
        Send an authenticated PUT request to fl33t

        :param str url: The URL to request
        :param kwargs: Any keyword args that :py:class:`requests.put` accepts
        :returns: :py:class:`requests.Response`
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        """
        return self._request('PUT', url, **kwargs)

    def delete(self, url, **kwargs):
        """
        Send an authenticated DELETE request to fl33t

        :param str url: The URL to request
        :param kwargs: Any keyword args that :py:class:`requests.delete`
            accepts
        :returns: :py:class:`requests.Response`
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        """
        return self._request('DELETE', url, **kwargs)

    def _request(self, method, url, **kwargs):
        """
        Wrapper for `requests` methods to include the bearer token
        If you need to make a call without the bearer token, make it
        directly against `requests`

        :param str method: The request method to use
        :param str url: The URL to request
        :param kwargs: Any keyword args that :py:module:`requests` methods
            accept
        :returns: :py:class:`requests.Response`
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
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

        self.logger.debug('Sending {} request with params: {}'.format(
            method, params))
        self.logger.debug('Sending {} request with payload: {}'.format(
            method, data))
        method = getattr(requests, method.lower())

        try:
            result = method(url, params=params, data=data, **kwargs)
            result.raise_for_status()

        except requests.exceptions.HTTPError as exc:
            if not isinstance(result, requests.Response):
                # The request failed in a way that we don't handle, give the
                # user the raised exception directly.
                raise

            if result.status_code in (401, 403):
                raise UnprivilegedToken(url)

            if result.status_code >= 500:
                # Raise that something went wrong with the fl33t API request
                message = '{} returned a {} error: {}'.format(
                    url,
                    result.status_code,
                    result.text)
                raise Fl33tApiException(message)

            if result.status_code not in (400, 404, 409):
                # Log the exception if the request failed with a status code
                # that we don't handle gracefully. 400/404 (InvalidIdError) and
                # 409 (DuplicateIdError) are meant to be handled by the caller.
                self.logger.exception(exc)

        return result

    def list_sessions(self, offset=None, limit=None):
        """
        List API Sessions

        :param offset: If provided, the starting offset for result sets.
            If not provided, will paginate through *all* records available,
            effectively ignoring the `limit` parameter. To only retrieve the
            first page of results, you must specifically set offset to `0`.
        :type offset: int or None
        :param limit: If provided, the number of records to return.
            Defaults to :py:attr:`default_query_limit`
        :type limit: int or None
        :yields: generator of `fl33t.models.Session`
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        """
        url = "/".join((self.base_team_url(), 'sessions'))
        params = self._build_offset_limit(offset=offset, limit=limit)

        single_page = False if offset is None else True
        return self._paginator(
            single_page,
            url,
            params,
            'session',
            Session,
            'listing sessions'
        )

    def get_own_session(self):
        """
        Return information about the current token

        :returns: :py:class:`fl33t.models.Session`
        :raises InvalidSessionIdError: if the session token does not exist
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        """

        return self.get_session(self.token)

    def get_session(self, session_token):
        """
        Return information about a specific session_token

        :param str session_token: The session token that you want information
            about
        :returns: :py:class:`fl33t.models.Session`
        :raises InvalidSessionIdError: if the session token does not exist
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        """

        url = "/".join((self.base_team_url(), 'session/{}'.format(
            session_token)))

        result = self.get(url)
        if result.status_code in (400, 404):
            raise InvalidSessionIdError()

        if 'session' in result.json():
            session = result.json()['session']
            return Session(client=self, **session)

        raise Fl33tApiException(ENDPOINT_FAILED_MSG.format(
            'session retrieval'))

    def get_fleet(self, fleet_id):
        """
        Return information about a specific fleet

        :param str fleet_id: The fleet ID to retrieve information for
        :returns: :py:class:`fl33t.models.Fleet`
        :raises InvalidFleetIdError: if the fleet does not exist
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        """

        url = "/".join((self.base_team_url(), 'fleet/{}'.format(fleet_id)))

        result = self.get(url)

        if result.status_code in (400, 404):
            raise InvalidFleetIdError(fleet_id)

        if 'fleet' in result.json():
            fleet = result.json()['fleet']
            return Fleet(client=self, **fleet)

        raise Fl33tApiException(ENDPOINT_FAILED_MSG.format(
            'fleet retrieval'))

    def get_build(self, train_id, build_id):
        """
        Return information about a specific build

        :param str train_id: The train ID that owns the provided build ID
        :param str build_id: The build ID to retrieve information for
        :returns: :py:class:`fl33t.models.Build`
        :raises InvalidBuildIdError: if the build does not exist
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        """

        url = "/".join((self.base_team_url(), 'train/{}/build/{}'.format(
            train_id, build_id)))

        result = self.get(url)

        if result.status_code in (400, 404):
            raise InvalidBuildIdError('train={}:{}'.format(train_id, build_id))

        if 'build' in result.json():
            build = result.json()['build']
            return Build(client=self, **build)

        raise Fl33tApiException(ENDPOINT_FAILED_MSG.format(
            'build retrieval'))

    def get_train(self, train_id):
        """
        Return information about a specific train

        :param str train_id: The train ID to retrieve information for
        :returns: :py:class:`fl33t.models.Train`
        :raises InvalidTrainIdError: if the train does not exist
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        """

        url = "/".join((self.base_team_url(), 'train/{}'.format(
            train_id)))

        result = self.get(url)

        if result.status_code in (400, 404):
            raise InvalidTrainIdError(train_id)

        if 'train' in result.json():
            train = result.json()['train']
            return Train(client=self, **train)

        raise Fl33tApiException(ENDPOINT_FAILED_MSG.format(
            'train retrieval'))

    def get_device(self, device_id):
        """
        Get a device by ID from fl33t.

        :param str device_id: The device ID to retrieve information for
        :returns: :py:class:`fl33t.models.Device`
        :raises InvalidDeviceIdError: if the device does not exist
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        """

        url = "/".join((self.base_team_url(), 'device/{}'.format(
            device_id)))

        result = self.get(url)

        if result.status_code in (400, 404):
            raise InvalidDeviceIdError(device_id)

        if 'device' in result.json():
            device = result.json()['device']
            return Device(client=self, **device)

        raise Fl33tApiException(ENDPOINT_FAILED_MSG.format(
            'device retrieval'))

    def has_upgrade_available(self, device_id, currently_installed_id=None):
        """
        Does this device have pending firmware updates?

        :param str device_id: The device ID to check for updates
        :param currently_installed_id: If provided, the build ID currently
            installed on the device
        :type currently_installed_id: str or None
        :returns: :py:class:`fl33t.models.Build` or False
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        """

        url = '/'.join((self.base_team_url(), 'device/{}/build'.format(
            device_id)))

        params = None
        if currently_installed_id:
            params = {
                'installed_build_id': currently_installed_id
            }

        result = self.get(url, params=params)

        # No update available.
        if result.status_code == 204:
            return False

        if 'build' in result.json():
            build = result.json()['build']
            return self.Build(**build)

        raise Fl33tApiException(ENDPOINT_FAILED_MSG.format(
            'device firmware check'))

    def list_fleets(self, train_id=None, offset=None, limit=None):
        """
        Get all fleets from fl33t.

        :param train_id: If provided, limits the result set to fleets
            belonging to the specified train ID
        :type train_id: str or None
        :param offset: If provided, the starting offset for result sets.
            If not provided, will paginate through *all* records available,
            effectively ignoring the `limit` parameter. To only retrieve the
            first page of results, you must specifically set offset to `0`.
        :type offset: int or None
        :param limit: If provided, the number of records to return.
            Defaults to :py:attr:`default_query_limit`
        :type limit: int or None
        :yields: generator of :py:class:`fl33t.models.Fleet`
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        """

        url = "/".join((self.base_team_url(), 'fleets'))
        params = self._build_offset_limit(offset=offset, limit=limit)

        if train_id:
            params['train_id'] = train_id

        single_page = False if offset is None else True
        return self._paginator(
            single_page,
            url,
            params,
            'fleet',
            Fleet,
            'listing fleets'
        )

    def list_trains(self, offset=None, limit=None):
        """
        Get all trains from fl33t.

        :param offset: If provided, the starting offset for result sets.
            If not provided, will paginate through *all* records available,
            effectively ignoring the `limit` parameter. To only retrieve the
            first page of results, you must specifically set offset to `0`.
        :type offset: int or None
        :param limit: If provided, the number of records to return.
            Defaults to :py:attr:`default_query_limit`
        :type limit: int or None
        :yields: generator of :py:class:`fl33t.models.Train`
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        """

        url = "/".join((self.base_team_url(), 'trains'))
        params = self._build_offset_limit(offset=offset, limit=limit)

        single_page = False if offset is None else True
        return self._paginator(
            single_page,
            url,
            params,
            'train',
            Train,
            'listing trains'
        )

    def list_devices(self, fleet_id=None, offset=None, limit=None):
        """
        Get all devices from fl33t.

        :param fleet_id: If provided, limits the result set to devices in the
            specified fleet
        :type fleet_id: str or None
        :param offset: If provided, the starting offset for result sets.
            If not provided, will paginate through *all* records available,
            effectively ignoring the `limit` parameter. To only retrieve the
            first page of results, you must specifically set offset to `0`.
        :type offset: int or None
        :param limit: If provided, the number of records to return.
            Defaults to :py:attr:`default_query_limit`
        :type limit: int or None
        :yields: generator of :py:class:`fl33t.models.Device`
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        """

        url = "/".join((self.base_team_url(), 'devices'))
        params = self._build_offset_limit(offset=offset, limit=limit)
        if fleet_id:
            params['fleet_id'] = fleet_id

        single_page = False if offset is None else True
        return self._paginator(
            single_page,
            url,
            params,
            'device',
            Device,
            'listing devices'
        )

    def list_builds(self, train_id, version=None, offset=None, limit=None):
        """
        Get all builds from fl33t by train id.

        :param int train_id: The train_id that the builds are part of
        :param offset: If provided, the starting offset for result sets.
            If not provided, will paginate through *all* records available,
            effectively ignoring the `limit` parameter. To only retrieve the
            first page of results, you must specifically set offset to `0`.
        :type offset: int or None
        :param limit: If provided, the number of records to return.
            Defaults to :py:attr:`default_query_limit`
        :type limit: int or None
        :yields: generator of :py:class:`fl33t.models.Build`
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        """

        url = "/".join((self.base_team_url(), 'train/{}/builds'.format(
            train_id)))
        params = self._build_offset_limit(offset=offset, limit=limit)
        if version:
            params['version'] = version

        single_page = False if offset is None else True
        return self._paginator(
            single_page,
            url,
            params,
            'build',
            Build,
            'listing builds for train {}'.format(train_id)
        )

    def _paginator(self,
                   single_page,
                   url,
                   params,
                   model_name,
                   model,
                   error_msg):

        """
        Paginate through a specific listing endpoint.

        :param bool single_page: If we should be doing pagination, or simply
            returning the single page of results.
        :param str url: The URL to use for the page retrieval
        :param dict params: A :py:`dict` of parameteres to send with the
            request
        :param str model_name: The name of the model that will be used to
            return data
        :param model: The actual class to be used to return data
        :type model: Any subclass of :py:class:`fl33t.models.Base`
        :param str error_msg: The error message to return in the case of an
            API communication exception
        :yields: generator of the provided `model` type
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        """

        total_count = None

        plural_model = '{}s'.format(model_name)

        while True:
            result = self.get(url, params=params)
            data = result.json()
            if plural_model not in data:
                raise Fl33tApiException(ENDPOINT_FAILED_MSG.format(error_msg))

            record_count = 0

            for item in data[plural_model]:
                record_count += 1
                yield model(client=self, **item)

            if single_page:
                break

            total_returned = params['offset'] + record_count

            if total_count is None:
                if '{}_count'.format(model_name) in data:
                    total_count = data['{}_count'.format(model_name)]
                else:
                    total_count = 0

            if total_count > total_returned:
                params['offset'] = params['offset'] + params['limit']

            else:
                break
