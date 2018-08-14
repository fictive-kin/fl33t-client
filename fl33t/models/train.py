"""

Train Model

"""

import datetime

from fl33t.models.base import BaseModel
from fl33t.models.mixins import (
    ManyBuildsMixin,
    ManyFleetsMixin
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

    def _base_url(self):
        """Build the base URL for actions"""

        return '/'.join((self._client.base_team_url(), 'train'))

    def update(self):
        """Update this train"""

        url = "/".join((self._base_url(), self.train_id))

        result = self._client.put(url, data=self)
        if not result or result.status_code != 204:
            return False

        return self

    def delete(self):
        """Delete this train"""

        url = "/".join((self._base_url(), self.train_id))

        result = self._client.delete(url)
        return result.status_code == 204

    def create(self):
        """Create this train in fl33t"""

        url = self._base_url()

        result = self._client.post(url, data=self)
        if not result or 'train' not in result.json():
            self.logger.exception('Could not create train')
            return False

        data = result.json()['train']
        for key in data.keys():
            setattr(self, key, data[key])

        return self
