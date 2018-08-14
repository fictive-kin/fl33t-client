"""

Build model

"""

import datetime
import os

import requests

from fl33t.models.base import BaseModel
from fl33t.models.mixins import OneTrainMixin
from fl33t.utils import md5


class Build(BaseModel, OneTrainMixin):
    """The Fl33t Build model"""

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

    def __init__(self, **kwargs):
        # need to have both the full path, if provided and the basename to
        # the build file
        if 'filename' in kwargs and kwargs['filename']:
            self.fullpath = kwargs.get('filename')
            kwargs['filename'] = os.path.basename(self.fullpath)
            if 'md5sum' not in kwargs:
                kwargs['md5sum'] = md5(self.fullpath)
            if 'size' not in kwargs:
                kwargs['size'] = os.path.getsize(self.fullpath)

        super().__init__(**kwargs)

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

    def _base_url(self):
        """Build the base URL for actions"""

        return '/'.join((
            self._client.base_team_url(),
            'train/{}/build'.format(
                self.train_id
            )
        ))

    def update(self):
        """Update this build"""

        url = "/".join((self._base_url(), self.build_id))

        result = self._client.put(url, data=self)
        if not result or result.status_code != 204:
            return False

        return self

    def delete(self):
        """Delete this build from a Fl33t train"""

        url = "/".join((self._base_url(), self.build_id))

        result = self._client.delete(url)
        return result.status_code == 204

    def create(self):
        """Create this build record in fl33t and upload the new build file"""

        url = self._base_url()

        result = self._client.post(url, data=self)
        if not result or 'build' not in result.json():
            self.logger.exception(
                'Could not create build for: {}'.format(self.version))
            return False

        data = result.json()['build']
        for key in data.keys():
            setattr(self, key, data[key])

        if not self.upload_url:
            self.logger.exception(
                'Build creation worked, but no upload_url was'
                ' provided by fl33t for build: {}'.format(self.version))
            return self

        headers = {
            'Content-Type': 'application/octet-stream',
            'Content-Disposition': 'attachment; filename="{}"'.format(
                self.filename)
        }
        with open(self.fullpath, 'rb') as build_file:
            response = requests.put(
                self.upload_url,
                data=build_file.read(),
                headers=headers)

            if not response or response.status_code != 200:
                self.logger.exception(
                    'Failed to upload build file: {}'.format(self.version))
                return False

        return self
