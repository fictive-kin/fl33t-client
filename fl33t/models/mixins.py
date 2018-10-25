"""
Mixins

Reusable pieces for fl33t models
"""


class ManyDevicesMixin:  # pylint: disable=too-few-public-methods
    """For models with child devices"""

    def devices(self, offset=None, limit=None):
        """Return the child devices"""
        return self._client.list_devices(fleet_id=self.fleet_id,
                                         offset=offset,
                                         limit=limit)


class ManyBuildsMixin:  # pylint: disable=too-few-public-methods
    """For models with child builds"""

    def builds(self, offset=None, limit=None):
        """Return the child builds"""
        return self._client.list_builds(train_id=self.train_id,
                                        offset=offset,
                                        limit=limit)


class OneBuildMixin:  # pylint: disable=too-few-public-methods
    """For models with a build parent"""

    _build = None

    @property
    def build(self):
        """Return the parent build"""
        if not self.build_id:
            return None

        if not self._build or self.build_id != self._build.build_id:
            if hasattr(self, 'fleet') and self.fleet.train_id:
                train_id = self.fleet.train_id

            elif hasattr(self, 'train_id') and self.train_id:
                train_id = self.train_id

            else:
                return None

            self._build = self._client.get_build(train_id, self.build_id)

        return self._build


class OneTrainMixin:  # pylint: disable=too-few-public-methods
    """For models with a train parent"""

    _train = None

    @property
    def train(self):
        """Return the parent train"""

        if not self.train_id:
            return None

        if not self._train or self.train_id != self._train.train_id:
            self._train = self._client.get_train(self.train_id)

        return self._train


class ManyFleetsMixin:  # pylint: disable=too-few-public-methods
    """For models with child fleets"""

    def fleets(self, offset=None, limit=None):
        """Return the child fleets"""
        return self._client.list_fleets(train_id=self.train_id,
                                        offset=offset,
                                        limit=limit)


class OneFleetMixin:  # pylint: disable=too-few-public-methods
    """For models with a parent fleet"""

    _fleet = None

    @property
    def fleet(self):
        """Return the parent fleet"""

        if not self.fleet_id:
            return None

        if not self._fleet or self.fleet_id != self._fleet.fleet_id:
            self._fleet = self._client.get_fleet(self.fleet_id)

        return self._fleet
