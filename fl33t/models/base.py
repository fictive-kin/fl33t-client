"""
BaseModel

Has all common methods for Fl33t models
"""

import datetime
import json
import logging

from dateutil import parser

from fl33t.exceptions import Fl33tClientMissing
from fl33t.utils import ExtendedEncoder


class BaseModel():
    """The base model from which all Fl33t models should be extended"""

    _data = {}
    _booleans = []
    _ints = []
    _timestamps = []
    _enums = {}
    _client = None

    def __init__(self, **kwargs):
        self._client = kwargs.pop('client', None)

        self.logger = logging.getLogger(__name__)
        for key in self._defaults.keys():
            if key not in kwargs:
                self._data[key] = self._defaults[key]

            else:
                self.set_data(key, kwargs[key])

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

    def set_data(self, key, value):
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

    def create(self):
        """Calls API client create method"""

        if not self._client:
            raise Fl33tClientMissing()
        method = getattr(self._client,
                         '{}_create'.format(self.__class__.__name__.lower()))
        return method(self)

    def delete(self):
        """Calls API client delete method"""

        if not self._client:
            raise Fl33tClientMissing()
        method = getattr(self._client,
                         '{}_delete'.format(self.__class__.__name__.lower()))
        return method(self)

    def update(self):
        """Calls API client update method"""

        if not self._client:
            raise Fl33tClientMissing()
        method = getattr(self._client,
                         '{}_update'.format(self.__class__.__name__.lower()))
        return method(self)
