Getting Started
===============

You must already have a valid fl33t account, in order to use this client.
You will need to know the `team_id` assigned to you by fl33t, and you will
need to create a session token within the fl33t console for you to use with
this client. Various privilege levels are available, most non-informational
interactions will require that the session token have `admin` privileges, but
the selection of the specific privilege to assign to this new session token are
left up to the reader.

Basic Tutorial
--------------

Create a :py:class:`fl33t.Fl33tClient`::

    from fl33t import Fl33tClient

    client = Fl33tClient("team-id", "session-token")

Then list all trains, fleets and devices in your account::

    for train in client.list_trains():
        print(train)
        for fleet in train.fleets():
            print(fleet)
            for device in fleet.devices():
                print(device)
                fw_upgrade = device.upgrade_available()
                if fw_upgrade:
                    print(fw_upgrade)

Download and install
--------------------

This package is in the `Python Package Index <http://pypi.org/project/fl33t>`__,
so ``pip install fl33t`` should be enough.  You can also clone it on `Github
<http://github.com/fictivekin/fl33t-client>`__.

Licensing
---------

fl33t is distributed under the MIT License.
