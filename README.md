
# Fl33t API Client

The Fl33t API Client is a Python module for interacting with https://www.fl33t.com/. It requires Python 3+. 


## Example usage

```python

from fl33t import Fl33tClient

team_id = '<your-team-id>'
token = '<your-token>'

client = Fl33tClient(team_id, token)

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
