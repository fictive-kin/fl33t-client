"""
Utilities

Any utilities in use by the fl33t client
"""

import enum
import hashlib
import json
import uuid

from datetime import datetime, timedelta

import pytz


class ExtendedEncoder(json.JSONEncoder):
    """Encoder that supports various additional types that we care about."""

    # pylint: disable=too-many-return-statements,arguments-differ,method-hidden
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.replace(tzinfo=pytz.UTC).isoformat('T')
        if isinstance(obj, timedelta):
            return str(obj)
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, enum.Enum):
            return obj.value
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, Exception):
            return str(obj)

        return json.JSONEncoder.default(self, obj)


def md5(filename):
    """Hash function for files to be uploaded to Fl33t"""

    md5hash = hashlib.md5()
    with open(filename, "rb") as filehandle:
        for chunk in iter(lambda: filehandle.read(4096), b""):
            md5hash.update(chunk)
    return md5hash.hexdigest()
