
v0.6.0: Fl33t API changes

- PR #7 (Thanks to [@fl33t-code](https://github.com/fl33t-code) for these updates)
    - The build URLs were moved to the top level instead of being nested beneath `/train/<train_id>`. This was motivated by ergonomics: the client may want to get information about a build without having the train_id handy.
    - The `has_upgrade_available` has been renamed `checkin` and has been changed to a more generic checkin POST. This will allow for the addition of new features on our roadmap that include the device sending and receiving more data during each checkin.

- Addition of better exceptions for errors during build creation:
    - `BuildUploadError` now exists for when an error occurs during the upload of the firmware file. Previously, the create call would return `False`
    - `NoUploadUrlProvided` now exists for when the initial build creation in Fl33t fails to return an upload URL. Previously, the create call would return itself, as if nothing really went wrong.

- `offset` and `limit` are passed through to the paginator method now instead of duplicate assignments for `single_page` and `params`.
