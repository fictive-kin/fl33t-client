
Fl33t API Client
================

The Fl33t API Client is a Python module for interacting with fl33t_. It requires Python 3+. 

.. _fl33t: https://www.fl33t.com


Example usage
-------------

Setup a Fl33t client::

    from fl33t import Fl33tClient

    team_id = '<your-team-id>'
    token = '<your-token>'

    client = Fl33tClient(team_id, token)


Retrieve all trains/fleets/devices and if there are any upgrades pending::

    for train in client.list_trains():
        print(train)
        for fleet in train.fleets():
            print(fleet)
            for device in fleet.devices():
                print(device)
                fw_upgrade = device.checkin()
                if fw_upgrade:
                    print(fw_upgrade)


Upload new build to a train::

    train_id = '<your-train-id>'
    version = '<your-version-id>'
    filename = '<full/path/to/your-firmware-file>'

    build = client.Build(
        train_id=train_id,
        version=version,
        filename=filename
    )

    print(build.create())
