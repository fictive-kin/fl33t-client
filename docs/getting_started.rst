Getting Started
===============

In order to use this client, you must already have a valid fl33t account.
You will need to know the `team_id` assigned to you by fl33t, and you will
need to create a session token within the fl33t console for you to use with
this client. Various privilege levels are available. Most non-informational
interactions will require that the session token have `admin` privileges, but
the selection of the specific privilege to assign to this new session token are
left up to you.


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
                fw_upgrade = device.checkin()
                if fw_upgrade:
                    print(fw_upgrade)


Download and Install
--------------------

This package is in the `Python Package Index`_, thus ``pip install fl33t``
is all it takes to get setup. If you prefer the latest and greatest, you can
also clone it directly from Github_.


Licensing
---------

fl33t is distributed under the MIT License.


.. _Python Package Index: https://pypi.org/project/fl33t
.. _Github: https://github.com/fictivekin/fl33t-client
