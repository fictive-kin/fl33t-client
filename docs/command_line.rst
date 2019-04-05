Command-Line Usage
==================

There is a command line interface included in this package. It uses the Click_
command line builder, and can be either used directly, or imported into your
own command groups. As with usage of the main modules, you must already have a
fl33t_ account credentials.


Basic Usage
-----------

To use the provided command line directly in your shell, you can provide your
credentials in one of 2 ways: as options to the commands, or in your
environment. It is suggested that you use the environment variable method, but
the options method will override the environment variables if the need arises.

To use the environment variable method::

    export FL33T_TEAM_ID="team-id"
    export FL33T_SESSION_TOKEN="session-token"
    fl33t trains list

And to use the command line option method::

    fl33t --team-id "team-id" --session-token "session-token" trains list

It is important to note the order of options and commands when using the
command line options for providing team id and session token. They are options
that are supplied to the ``fl33t`` command, and as such, need to be
provided prior to the subcommand (in this case, ``trains``). This is a
requirement of ``Click``.

Due to the use of Click_, there is also help available for commands and all
subcommands::

    fl33t --help
    fl33t trains --help
    fl33t trains list --help

Each of the ``fl33t`` models is exposed as a subcommand:

- ``builds``
- ``devices``
- ``fleets``
- ``trains``
- ``sessions``

Each of the model specific subcommands provides 5 actions:

- ``list``
- ``show``
- ``create``
- ``update``
- ``delete``

Every model action has it's own specific options that can be explored with the
``--help`` option.


Importing
---------

If you already have your own commands setup, and would like to integrate these
into your pre-existing system, it is easily accomplished, provided that you
are already using Click_.

In your exposed CLI commands::

    from fl33t.cli import cli as fl33t_cmds

    mycli.add_command(fl33t_cmds, name='fl33t')


.. _Click: https://pypi.org/project/click/
.. _fl33t: https://www.fl33t.com
