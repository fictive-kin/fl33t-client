
class ManyDevicesMixin:
    def devices(self):
        return self._client.list_devices(fleet_id=self.fleet_id)

class ManyBuildsMixin:
    def builds(self):
        return self._client.list_builds(train_id=self.train_id)

class OneBuildMixin:
    def build(self):
        return self._client.get_build(self.build_id)

class OneTrainMixin:
    def train(self):
        return self._client.get_train(self.train_id)

class ManyFleetsMixin:
    def fleets(self):
        return self._client.list_fleets(train_id=self.train_id)

class OneFleetMixin:
    def fleet(self):
        return self._client.get_fleet(self.fleet_id)
