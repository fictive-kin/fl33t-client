"""

Models

All the models in use by fl33t

"""

from fl33t.exceptions import InvalidFleetIdError
from fl33t.models.base import BaseModel
from fl33t.models.mixins import (
    OneBuildMixin,
    ManyDevicesMixin,
    OneTrainMixin
)


# pylint: disable=no-member
class Fleet(BaseModel, OneTrainMixin, OneBuildMixin, ManyDevicesMixin):
    """The fl33t Fleet model"""

    _invalid_id = InvalidFleetIdError

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

    def id(self):
        """
        Get this fleet's unique ID

        :returns: str
        """

        return self.fleet_id

    def _self_url(self):
        """
        The full URL for this fleet in fl33t

        :returns: str
        """

        return '/'.join((self._base_url(), self.fleet_id))
