"""

Models

All the models in use by Fl33t

"""

import datetime

from fl33t.models.base import BaseModel
from fl33t.models.build import Build # noqa
from fl33t.models.mixins import (
    OneBuildMixin,
    ManyBuildsMixin,
    ManyDevicesMixin,
    OneTrainMixin,
    OneFleetMixin,
    ManyFleetsMixin
)


class Session(BaseModel):
    """The Fl33t Session model"""

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
        """Return a human readable privilege"""
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
        return 'unprivileged'

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
    """The Fl33t Fleet model"""

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
        return ('<Fleet id={} name={} train_id={} unreleased={} '
                'size={}>'.format(
                    self.fleet_id,
                    self.name,
                    self.train_id,
                    self.unreleased,
                    self.size
                    )
                )


class Device(BaseModel, OneBuildMixin, OneFleetMixin):
    """The Fl33t Device model"""
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
            return self._client.has_firmware_update(
                self.device_id,
                self.build_id)
        return self._client.has_firmware_update(self.device_id)

    def __str__(self):
        return 'Device {}: {} (Fleet: {}, Build: {})'.format(
            self.device_id,
            self.name,
            self.fleet_id,
            self.build_id
        )

    def __repr__(self):
        return ('<Device id={} name={} fleet_id={} build_id={} '
                'last_seen={}>'.format(
                    self.device_id,
                    self.name,
                    self.fleet_id,
                    self.build_id,
                    self.checkin_tstamp
                    )
                )


class Train(BaseModel, ManyFleetsMixin, ManyBuildsMixin):
    """The Fl33t Train model"""

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
