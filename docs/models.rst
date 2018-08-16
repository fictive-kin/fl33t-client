Models
======

These are the data models in use within the fl33t module.

.. autoclass:: fl33t.models.build.Build
    :inherited-members:

    :param client: The API client to route requests through
    :type client: :py:class:`fl33t.client.Fl33tClient` or None
    :param str build_id: The build ID in fl33t for this build
    :param str download_url: URL provided by fl33t, valid for 3 minutes, to download this build
    :param str filename: The file name that the build download will have or has
    :param str md5sum: The MD5 hash of the build file for integrity checks
    :param bool released: Has this build been released?
    :param int size: The size of the build file
    :param str status: The status of the build file itself, can be one of: created, available, failed
    :param str train_id: The fl33t train ID that this build belongs to
    :param upload_tstamp: The datetime that this build was uploaded to fl33t
    :type upload_tstamp: str, :py:class:`datetime.datetime` or None
    :param str upload_url: A temporary URL to upload a newly created build to
    :param str version: The version string to use within fl33t for this build

.. autoclass:: fl33t.models.device.Device
    :inherited-members:

    :param client: The API client to route requests through
    :type client: :py:class:`fl33t.client.Fl33tClient` or None
    :param str device_id: The device ID in fl33t for this device
    :param str build_id: The fl33t build ID that this device is using
    :param checkin_tstamp: The datetime that this device was last seen by fl33t
    :type checkin_tstamp: str, :py:class:`datetime.datetime` or None
    :param str fleet_id: The fl33t fleet ID that this build belongs to
    :param str name: The name of the device in fl33t
    :param str session_token: The device's session token

.. autoclass:: fl33t.models.fleet.Fleet
    :inherited-members:

    :param client: The API client to route requests through
    :type client: :py:class:`fl33t.client.Fl33tClient` or None
    :param str fleet_id: The fleet ID in fl33t for this fleet
    :param str build_id: The fl33t build ID that devices in this fleet should install
    :param str name: The name of the fleet in fl33t
    :param int size: The number of devices in this fleet
    :param str train_id: The fl33t train ID that this fleet belongs to
    :param bool unreleased: Should this fleet auto-update to unreleased builds

.. autoclass:: fl33t.models.session.Session
    :inherited-members:

    :param client: The API client to route requests through
    :type client: :py:class:`fl33t.client.Fl33tClient` or None
    :param bool admin: Is this session admin privileged?
    :param bool device: Is this session device privileged?
    :param bool provisioning: Is this session provisioning privileged?
    :param bool readonly: Is this session readonly privileged?
    :param str session_token: The fl33t session token
    :param str type: The type of session this is, can be one of: account, device, api
    :param bool upload: Is this session upload privileged?

.. autoclass:: fl33t.models.train.Train
    :inherited-members:

    :param client: The API client to route requests through
    :type client: :py:class:`fl33t.client.Fl33tClient` or None
    :param str train_id: The train ID in fl33t for this train
    :param str name: The name of the train in fl33t
    :param upload_tstamp: Most recent upload_tstamp from all builds in this train
    :type upload_tstamp: str, :py:class:`datetime.datetime` or None
