"""

Models

All the models in use by Fl33t

"""

from fl33t.models.base import BaseModel


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

    def _base_url(self):
        """Build the base URL for actions"""

        return '/'.join((self._client.base_team_url(), 'session'))

    def update(self):
        """Update this session"""

        url = "/".join((self._base_url(), self.session_token))

        result = self._client.put(url, data=self)
        if not result or result.status_code != 204:
            return False

        return self

    def delete(self):
        """Delete this session"""

        url = "/".join((self._base_url(), self.session_token))

        result = self._client.delete(url)
        return result.status_code == 204

    def create(self):
        """Create this session in fl33t"""

        url = self._base_url()

        result = self._client.post(url, data=self)
        if not result or 'session' not in result.json():
            self.logger.exception(
                'Could not create session')
            return False

        data = result.json()['session']
        for key in data.keys():
            setattr(self, key, data[key])

        return self
