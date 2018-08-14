"""

Models

All the models in use by Fl33t

"""

from fl33t.models.base import BaseModel
from fl33t.models.mixins import (
    OneBuildMixin,
    ManyDevicesMixin,
    OneTrainMixin
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

    def _base_url(self):
        """Build the base URL for actions"""

        return '/'.join((self._client.base_team_url(), 'fleet'))

    def update(self):
        """Update this fleet"""

        url = "/".join((self._base_url(), self.fleet_id))

        result = self._client.put(url, data=self)
        if not result or result.status_code != 204:
            return False

        return self

    def delete(self):
        """Delete this fleet"""

        url = "/".join((self._base_url(), self.fleet_id))

        result = self._client.delete(url)
        return result.status_code == 204

    def create(self):
        """Create this fleet in fl33t"""

        url = self._base_url()

        result = self._client.post(url, data=self)
        if not result or 'fleet' not in result.json():
            self.logger.exception('Could not create fleet')
            return False

        data = result.json()['fleet']
        for key in data.keys():
            setattr(self, key, data[key])

        return self
