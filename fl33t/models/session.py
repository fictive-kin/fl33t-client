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
        'name': '',
        'admin': False,
        'device': False,
        'provisioning': False,
        'readonly': False,
        'session_token': '',
        'type': '',
        'upload': False
    }

    @property
    def priv(self):
        """
        Return a human-readable privilege

        :returns: str
        """
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
        return 'Session {} (Type: {} Privilege: {})'.format(
            self.name,
            self.type,
            self.priv
        )

    def __repr__(self):
        return '<Session name={} type={} priv={}>'.format(
            self.name,
            self.type,
            self.priv
        )

    @property
    def id(self):
        """
        Get this session's unique ID

        :returns: str
        """

        return self.session_token

    @property
    def self_url(self):
        """
        The full URL for this particular session in fl33t

        :returns: str
        """

        return '/'.join((self.base_url, self.session_token))
