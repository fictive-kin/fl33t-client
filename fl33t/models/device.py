"""

Models

All the models in use by fl33t

"""

import datetime

from fl33t.exceptions import (
    Fl33tClientException,
    InvalidDeviceIdError,
    DuplicateDeviceIdError
)
from fl33t.models.base import BaseModel
from fl33t.models.mixins import (
    OneBuildMixin,
    OneFleetMixin
)


# pylint: disable=no-member
class Device(BaseModel, OneBuildMixin, OneFleetMixin):
    """
    The fl33t Device model
    """

    invalid_id = InvalidDeviceIdError
    _timestamps = ['checkin_tstamp']

    _defaults = {
        'build_id': '',
        'checkin_tstamp': datetime.datetime.utcnow(),
        'device_id': '',
        'fleet_id': '',
        'name': '',
        'session_token': ''
    }

    def __init__(self, client=None, **kwargs):
        if client:
            device_id = kwargs.pop('device_id', client.generate_id_string())
            kwargs['device_id'] = device_id
        elif 'device_id' not in kwargs:
            raise ValueError(('No device_id was provided, nor an API client '
                              'to generate and ID'))
        super().__init__(client=client, **kwargs)

    def id(self):
        """
        Get this Device's unique ID

        :returns: str
        """

        return self.device_id

    def upgrade_available(self, installed_build_id=None):
        """
        Returns the available firmware update, if there is one

        :param installed_build_id: The currently installed build ID, if known
        :type installed_build_id: str or None
        :returns: :py:class:`fl33t.models.Build`, if upgrade available or
            False, if none
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        :raises Fl33tClientException: if the model was instantiated without a
            :py:class:`fl33t.Fl33tClient`
        """

        if not self._client:
            raise Fl33tClientException()

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

    def _self_url(self):
        """
        The full URL for this object in fl33t

        :returns: str
        """

        return '/'.join((
            self._base_url(),
            self.device_id
        ))

    def create(self):
        """
        Create this device in fl33t

        :returns: :py:class:`self` on success, or False on failure
        :raises DuplicateDeviceIdError: if the device ID already exists
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        :raises Fl33tClientException: if the model was instantiated without a
            :py:class:`fl33t.Fl33tClient`
        """

        if not self._client:
            raise Fl33tClientException()

        url = self._base_url()

        result = self._client.post(url, data=self)
        if result.status_code == 409:
            raise DuplicateDeviceIdError(self.device_id)

        if 'device' not in result.json():
            self.logger.exception('Could not create device')
            return False

        data = result.json()['device']
        for key in data.keys():
            setattr(self, key, data[key])

        return self
