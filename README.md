
# Fl33t API Client

The Fl33t API Client is a Python module for interacting with https://www.fl33t.com/. It requires Python 3+. 


## Example usage

Setup a Fl33t client

```python

from fl33t import Fl33tClient

team_id = '<your-team-id>'
token = '<your-token>'

client = Fl33tClient(team_id, token)

```


Retrieve all trains/fleets/devices and if there are any upgrades pending

```python

for train in client.list_trains():
    print(train)
    for fleet in train.fleets():
        print(fleet)
        for device in fleet.devices():
            print(device)
            fw_upgrade = device.upgrade_available()
            if fw_upgrade:
                print(fw_upgrade)

```


Upload new build to a train:

```python

train_id = '<your-train-id>'
version = '<your-version-id>'
filename = '<full/path/to/your-firmware-file>'

build = client.Build(
    train_id=train_id,
    version=version,
    filename=filename
)

print(build.create())

```
