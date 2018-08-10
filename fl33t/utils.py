
import enum
import hashlib
import json
import pytz
import uuid

from datetime import datetime, timedelta

class ExtendedEncoder(json.JSONEncoder):
    """Encoder that supports various additional types that we care about."""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.replace(tzinfo=pytz.UTC).isoformat('T')
        if isinstance(obj, timedelta):
            return str(obj)
        if isinstance(obj, uuid.UUID):
            return unicode(obj)
        if isinstance(obj, enum.Enum):
            return obj.value
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, Exception):
            return unicode(obj)

        return json.JSONEncoder.default(self, obj)


def md5(filename):
    md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5.update(chunk)
    return md5.hexdigest()
