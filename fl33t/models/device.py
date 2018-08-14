"""

Models

All the models in use by Fl33t

"""

import datetime

from fl33t.exceptions import (
    InvalidDeviceIdError,
    DuplicateDeviceIdError
)
from fl33t.models.base import BaseModel
from fl33t.models.mixins import (
    OneBuildMixin,
    OneFleetMixin
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

    def __init__(self, **kwargs):
        client = kwargs.get('client')
        if client:
            device_id = kwargs.pop('device_id', client.generate_id_string())
            kwargs['device_id'] = device_id
        elif 'device_id' not in kwargs:
            raise ValueError(('No device_id was provided, nor an API client '
                              'to generate and ID'))
        super().__init__(**kwargs)

    def upgrade_available(self, installed_build_id=None):
        """Returns the available firmware update, if there is one"""

        if not installed_build_id and self.build_id:
            installed_build_id = self.build_id

        return self._client.has_upgrade_available(
            self.device_id,
            currently_installed_id=installed_build_id
        )

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

    def _base_url(self):
        """Build the base URL for actions"""

        return '/'.join((self._client.base_team_url(), 'device'))

    def update(self):
        """Update this device"""

        url = "/".join((self._base_url(), self.device_id))

        result = self._client.put(url, data=self)
        if not result or result.status_code != 204:
            return False

        return self

    def delete(self):
        """Delete this device"""

        url = "/".join((self._base_url(), self.device_id))

        result = self._client.delete(url)

        if result.status_code == 400:
            raise InvalidDeviceIdError(self.device_id)

        return result.status_code == 204

    def create(self):
        """Create this device in fl33t"""

        url = self._base_url()

        result = self._client.post(url, data=self)
        if not result:
            self.logger.exception('Could not create device')
            return False

        if result.status_code == 409:
            raise DuplicateDeviceIdError(self.device_id)

        if 'device' not in result.json():
            self.logger.exception('Could not create device')
            return False

        data = result.json()['device']
        for key in data.keys():
            setattr(self, key, data[key])

        return self
