"""

Train Model

"""

import datetime

from fl33t.exceptions import InvalidTrainIdError
from fl33t.models.base import BaseModel
from fl33t.models.mixins import (
    ManyBuildsMixin,
    ManyFleetsMixin
)


# pylint: disable=no-member
class Train(BaseModel, ManyFleetsMixin, ManyBuildsMixin):
    """
    The fl33t Train model
    """

    _invalid_id = InvalidTrainIdError

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

    def id(self):
        """
        Get this train's unique ID

        :returns: str
        """

        return self.train_id

    def _self_url(self):
        """
        The full URL for this train in fl33t

        :returns: str
        """

        return '/'.join((self._base_url(), self.train_id))
