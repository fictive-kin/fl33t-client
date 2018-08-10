
import datetime
import os

from fl33t.models.base import BaseModel
from fl33t.models.mixins import (
    OneBuildMixin,
    ManyBuildsMixin,
    ManyDevicesMixin,
    OneTrainMixin,
    OneFleetMixin,
    ManyFleetsMixin
)
from fl33t.utils import md5

class Session(BaseModel):
    _booleans = ['admin', 'device', 'provisioning', 'readonly', 'upload']

    _defaults = {
        'admin': False,
        'device': False,
        'provisioning': False,
        'readonly': False,
        'session_token': '',
        'type': '',
        'upload': False
    }

    def priv(self):
        if self.admin:
            return 'admin'
        if self.device:
            return 'device'
        if self.provisioning:
            return 'provisioning'
        if self.upload:
            return 'upload'
        if self.readonly:
            return 'readonly'

    def __str__(self):
        return '{}:{}:{}'.format(
            self.type,
            self.priv(),
            self.session_token
        )

    def __repr__(self):
        return '<Session type={} priv={} token={}>'.format(
            self.type,
            self.priv(),
            self.session_token
        )


class Fleet(BaseModel, OneTrainMixin, OneBuildMixin, ManyDevicesMixin):
    _booleans = ['unreleased']
    _ints = ['size']

    _defaults = {
        'build_id': None,
        'fleet_id': '',
        'name': '',
        'size': 0,
        'train_id': '',
        'unreleased': True
    }

    def __str__(self):
        return 'Fleet {}: {} (Train: {}, Status: {}, Size: {})'.format(
            self.fleet_id,
            self.name,
            self.train_id,
            'Unreleased' if self.unreleased else 'Released',
            self.size
        )

    def __repr__(self):
        return '<Fleet id={} name={} train_id={} unreleased={} size={}>'.format(
            self.fleet_id,
            self.name,
            self.train_id,
            self.unreleased,
            self.size
        )


class Device(BaseModel, OneBuildMixin, OneFleetMixin):
    _timestamps = ['checkin_tstamp']

    _defaults = {
        'build_id': '',
        'checkin_tstamp': datetime.datetime.utcnow(),
        'device_id': '',
        'fleet_id': '',
        'name': '',
        'session_token': ''
    }

    def upgrade_available(self):
        """Returns the available firmware update, if there is one"""
        if self.build_id:
            return self._client.has_firmware_update(self.device_id, self.build_id)
        return self._client.has_firmware_update(self.device_id)

    def __str__(self):
        return 'Device {}: {} (Fleet: {}, Build: {})'.format(
            self.device_id,
            self.name,
            self.fleet_id,
            self.build_id
        )

    def __repr__(self):
        return '<Device id={} name={} fleet_id={} build_id={}, last_seen={})'.format(
            self.device_id,
            self.name,
            self.fleet_id,
            self.build_id,
            self.checkin_tstamp
        )


class Build(BaseModel, OneTrainMixin):
    _booleans = ['released']
    _enums = {
        'status': ['created', 'failed', 'available']
    }
    _ints = ['size']
    _timestamps = ['upload_tstamp']

    _defaults = {
        'build_id': '',
        'download_url': '',
        'filename': '',
        'md5sum': '',
        'released': False,
        'size': 0,
        'status': '',
        'train_id': '',
        'upload_tstamp': datetime.datetime.utcnow(),
        'upload_url': '',
        'version': ''
    }

    fullpath = None

    def __init__(self, **kwargs):
        # need to have both the full path, if provided and the basename to
        # the build file
        if 'filename' in kwargs and kwargs['filename']:
            self.fullpath = kwargs.get('filename')
            kwargs['filename'] = os.path.basename(self.fullpath)
            if 'md5sum' not in kwargs:
                kwargs['md5sum'] = md5(self.fullpath)
            if 'size' not in kwargs:
                kwargs['size'] = os.path.getsize(self.fullpath)

        super().__init__(**kwargs)

    def __str__(self):
        return ('Build {}: {} (Status: {}, Released: {}, Train: {}, Size: {},'
                ' Uploaded: {})'.format(
            self.build_id,
            self.version,
            self.status,
            'Released' if self.released else 'Unreleased',
            self.train_id,
            self.size,
            self.upload_tstamp
        ))

    def __repr__(self):
        return '<Build id={} version={} md5sum={} size={} train_id={} uploaded={}'.format(
            self.build_id,
            self.version,
            self.md5sum,
            self.size,
            self.train_id,
            self.upload_tstamp
        )


class Train(BaseModel, ManyFleetsMixin, ManyBuildsMixin):
    _timestamps = ['upload_tstamp']

    _defaults = {
        'train_id': '',
        'name': '',
        'upload_tstamp': datetime.datetime.utcnow()
    }

    def __str__(self):
        return 'Train {}: {}'.format(self.train_id, self.name)

    def __repr__(self):
        return '<Train id={} name={} latest_build={}>'.format(
            self.train_id,
            self.name,
            self.upload_tstamp
        )
