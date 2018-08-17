"""
BaseModel

Has all common methods for Fl33t models
"""

import datetime
import json
import logging

from abc import ABC, abstractmethod
from dateutil import parser

from fl33t.exceptions import Fl33tClientException, InvalidIdError
from fl33t.utils import ExtendedEncoder


class BaseModel(ABC):
    """The base model from which all Fl33t models should be extended"""

    _invalid_id = InvalidIdError
    _data = {}
    _booleans = []
    _ints = []
    _timestamps = []
    _enums = {}
    _client = None

    def __init__(self, client=None, **kwargs):
        self._client = client

        self.logger = logging.getLogger(__name__)
        for key in self._defaults.keys():
            if key not in kwargs:
                self._data[key] = self._defaults[key]

            else:
                self._set_data(key, kwargs[key])

    def to_json(self):
        """Dumps this model as JSON for use in API calls"""

        return json.dumps(
            {
                self.__class__.__name__.lower(): self._data
            },
            cls=ExtendedEncoder)

    def __getattr__(self, key, default=None):
        if key not in self._data:
            if not default:
                raise AttributeError(
                    '{} is not a valid attribute of {}'.format(
                        key, self.__class__.__name__))
            return default

        return self._data.get(key, default)

    def _set_data(self, key, value):
        """Sets a value within the model's allowed properties"""

        if key not in self._defaults:
            raise AttributeError('{} is not a valid attribute of {}'.format(
                key, self.__class__.__name__))
        if not value:
            self._data[key] = value

        elif key in self._booleans:
            self._data[key] = bool(value)

        elif key in self._ints:
            self._data[key] = int(value)

        elif key in self._timestamps:
            try:
                if not value:
                    # If it evaluates to false, just use whatever
                    # was passed
                    self._data[key] = value
                elif isinstance(value, datetime.datetime):
                    self._data[key] = value
                else:
                    self._data[key] = parser.parse(value)
            except Exception:
                raise ValueError('{} MUST be an instance of'
                                 ' datetime.datetime or be machine'
                                 ' parsable'.format(key))

        elif key in self._enums:
            if value not in self._enums[key]:
                raise ValueError('{} MUST be one of {}'.format(
                    key, self._enums[key]))
            self._data[key] = value

        else:
            self._data[key] = value

    @abstractmethod
    def id(self):  # pylint: disable=invalid-name
        """
        Return the unique ID of this object

        In the case that this object requires a parent ID element for
            uniqueness, this should return the IDs in order, as required,
            for human readability:
            - `<parent-type>=<parent>:<child>`
            - `<grandparent-type>=<grandparent>:<parent-type>=<parent>:<child>`

        :returns: str
        """
        pass

    @abstractmethod
    def _self_url(self):
        """
        For objects that exist in fl33t, the full URL for REST queries

        :returns: str
        """
        pass

    def _base_url(self):
        """
        Build the base URL for actions

        :returns: str
        """

        return '/'.join((
            self._client.base_team_url(),
            self.__class__.__name__.lower()
        ))

    def update(self):
        """
        Update this object in fl33t

        :returns: :py:class:`self`, on success or False, on update failure
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        :raises Fl33tClientException: if the model was instantiated without a
            :py:class:`fl33t.Fl33tClient`
        """

        if not self._client:
            raise Fl33tClientException()

        result = self._client.put(self._self_url(), data=self)
        if result.status_code in [400, 404]:
            raise self._invalid_id(self.id)

        if result.status_code != 204:
            self.logger.warning('Received {}: {}'.format(
                result.status_code, result.text))
            return False

        return self

    def delete(self):
        """
        Delete this object from a fl33t

        :returns: True, on success or False, on failure
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        :raises Fl33tClientException: if the model was instantiated without a
            :py:class:`fl33t.Fl33tClient`
        """

        if not self._client:
            raise Fl33tClientException()

        result = self._client.delete(self._self_url())

        if result.status_code in [400, 404]:
            raise self._invalid_id(self.id)

        if result.status_code != 204:
            self.logger.warning('Received {}: {}'.format(
                result.status_code, result.text))
            return False

        return True

    def create(self):
        """
        Create this object in fl33t

        :returns: :py:class:`self`, on success or False, on failure
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        :raises Fl33tClientException: if the model was instantiated without a
            :py:class:`fl33t.Fl33tClient`
        """

        if not self._client:
            raise Fl33tClientException()

        class_name = self.__class__.__name__.lower()
        url = self._base_url()

        result = self._client.post(url, data=self)
        if class_name not in result.json():
            self.logger.exception('Could not create {}'.format(class_name))
            return False

        data = result.json()[class_name]
        for key in data.keys():
            setattr(self, key, data[key])

        return self
