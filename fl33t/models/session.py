"""

Models

All the models in use by fl33t

"""

from fl33t.exceptions import InvalidSessionIdError
from fl33t.models.base import BaseModel


# pylint: disable=no-member
class Session(BaseModel):
    """The fl33t Session model"""

    _invalid_id = InvalidSessionIdError
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
        """Return a human-readable privilege"""
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

    def id(self):
        """
        Get this session's unique ID

        :returns: str
        """

        return self.session_token

    def _self_url(self):
        """
        The full URL for this session in fl33t

        :returns: str
        """

        return '/'.join((self._base_url(), self.session_token))
