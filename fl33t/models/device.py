"""

Models

All the models in use by Fl33t

"""

import datetime

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

    def upgrade_available(self):
        """Returns the available firmware update, if there is one"""
        url = '/'.join((self._base_url(), '{}/build'.format(self.device_id)))
        params = None

        if self.build_id:
            params = {
                'installed_build_id': self.build_id
            }

        result = self._client.get(url, params=params)
        if result:
            # No update available.
            if result.status_code == 204:
                return False

            if 'build' in result.json():
                build = result.json()['build']
                return self._client.Build(**build)

        return False

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
        return result.status_code == 204

    def create(self):
        """Create this device in fl33t"""

        url = self._base_url()

        result = self._client.post(url, data=self)
        if not result or 'device' not in result.json():
            self.logger.exception('Could not create device')
            return False

        data = result.json()['device']
        for key in data.keys():
            setattr(self, key, data[key])

        return self
