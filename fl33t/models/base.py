
import datetime

from dateutil import parser

class BaseModel():
    _data = {}
    _booleans = []
    _ints = []
    _timestamps = []
    _enums = {}
    _client = None

    def __init__(self, **kwargs):
        self._client = kwargs.pop('client', None)

        for key in self._defaults.keys():
            if key not in kwargs:
                self._data[key] = self._defaults[key]

            else:
                if key in self._booleans:
                    self._data[key] = bool(kwargs[key])

                elif key in self._ints:
                    self._data[key] = int(kwargs[key])

                elif key in self._timestamps:
                    try:
                        if not kwargs[key]:
                            # If it evaluates to false, just use whatever
                            # was passed
                            self._data[key] = kwargs[key]
                        elif isinstance(kwargs[key], datetime.datetime):
                            self._data[key] = kwargs[key]
                        else:
                            self._data[key] = parser.parse(kwargs[key])
                    except:
                        raise ValueError('{} MUST be an instance of'
                                         ' datetime.datetime or be machine'
                                         ' parsable'.format(key))

                elif key in self._enums:
                    if kwargs[key] not in self._enums[key]:
                        raise ValueError('{} MUST be one of {}'.format(
                            key, self._enums[key]))
                    self._data[key] = kwargs[key]

                else:
                    self._data[key] = kwargs[key]


    def __getattr__(self, key, default=None):
        if key not in self._data:
            if not default:
                raise AttributeError('{} is not a valid attribute of {}'.format(
                          key, self.__class__.__name__))
            return default

        return self._data.get(key, default)
