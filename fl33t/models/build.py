"""

Build model

"""

import datetime
import os

import requests

from fl33t.exceptions import (
    Fl33tClientException,
    BuildUploadError,
    InvalidBuildIdError,
    NoUploadUrlProvidedError
)
from fl33t.models.base import BaseModel
from fl33t.models.mixins import OneTrainMixin
from fl33t.utils import md5


# pylint: disable=no-member
class Build(BaseModel, OneTrainMixin):
    """
    The fl33t Build model
    """

    _invalid_id = InvalidBuildIdError

    _booleans = ['released']
    _enums = {
        'status': ['created', 'failed', 'available']
    }
    _ints = ['size']
    _timestamps = ['upload_tstamp']

    _defaults = {
        'build_id': '',
        'download_url': '',
        'filename': '',
        'md5sum': '',
        'released': False,
        'size': 0,
        'status': '',
        'train_id': '',
        'upload_tstamp': datetime.datetime.utcnow(),
        'upload_url': '',
        'version': ''
    }

    fullpath = None

    def __init__(self, client=None, **kwargs):
        # need to have both the full path, if provided and the basename to
        # the build file
        if 'filename' in kwargs and kwargs['filename']:
            self.fullpath = kwargs.get('filename')
            kwargs['filename'] = os.path.basename(self.fullpath)
            if 'md5sum' not in kwargs:
                kwargs['md5sum'] = md5(self.fullpath)
            if 'size' not in kwargs:
                kwargs['size'] = os.path.getsize(self.fullpath)

        super().__init__(client=client, **kwargs)

    def __str__(self):
        return ('Build {}: {} (Status: {}, Released: {}, Train: {}, Size: {},'
                ' Uploaded: {})'.format(
                    self.build_id,
                    self.version,
                    self.status,
                    'Released' if self.released else 'Unreleased',
                    self.train_id,
                    self.size,
                    self.upload_tstamp
                    )
                )

    def __repr__(self):
        return '<Build id={} version={} train_id={} uploaded={}>'.format(
            self.build_id,
            self.version,
            self.train_id,
            self.upload_tstamp
            )

    @property
    def id(self):
        """
        Get this build's unique ID

        :returns: str
        """

        return self.build_id

    @property
    def self_url(self):
        """
        The full URL for this particular build in fl33t

        :returns: str
        """

        return '/'.join((
            self.base_url,
            self.build_id
        ))

    @property
    def base_url(self):
        """
        The base URL for build actions

        :returns: str
        """

        return '/'.join((
            self._client.base_team_url,
            'build'
        ))

    def create(self):
        """
        Create this build record in fl33t and upload the new build file

        :returns: :py:class:`self` on success, or False on failure
        :raises UnprivilegedToken: if the session token does not have enough
            privilege to perform this action
        :raises Fl33tApiException: if there was a 5xx error returned by fl33t
        :raises Fl33tClientException: if the model was instantiated without a
            :py:class:`fl33t.Fl33tClient`
        :raises NoUploadUrlProvidedError: if the create response from the fl33t
            API did not include an upload URL
        :raises BuildUploadError: if an error occurred when uploading the
            firmware file to the fl33t provided upload URL
        """

        if not self._client:
            raise Fl33tClientException()

        result = self._client.post(self.base_url, data=self)
        if 'build' not in result.json():
            self.logger.exception(
                'Could not create build for: {}'.format(self.version))
            return False

        data = result.json()['build']
        for key in data.keys():
            if key in ['filename', 'size']:
                # Allowing the filename to be overridden will break the upload
                # and size is unknown to the fl33t API at this point, so leave
                # it as was passed in to (or determined by) the object
                continue
            setattr(self, key, data[key])

        if not self.upload_url:
            raise NoUploadUrlProvidedError()

        # The Content-Disposition header is what sets the filename in fl33t
        headers = {
            'Content-Type': 'application/octet-stream',
            'Content-Disposition': 'attachment; filename="{}"'.format(
                self.filename)
        }
        with open(self.fullpath, 'rb') as build_file:
            # Must use requests directly as we do not want the normal fl33t
            # API headers to be added to the upload request. The upload_url is
            # a pre-signed URL and as such has all authentication built-in.
            response = requests.put(
                self.upload_url,
                data=build_file.read(),
                headers=headers)

            # Any non-200 status is an error with the upload.
            if not response or response.status_code != 200:
                raise BuildUploadError()

        return self
