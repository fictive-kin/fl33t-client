"""
fl33t.cli.click

Command line interaction helpers for apps using Click
"""

import os
import sys

import click

from fl33t import Fl33tClient
from fl33t.cli.commands.fleets import cli as fleets_cmds
from fl33t.cli.commands.trains import cli as trains_cmds


clients = {}

def create_client(team_id, session_token):
    if not team_id:
        team_id = os.environ.get('FL33T_TEAM_ID')
    if not session_token:
        session_token = os.environ.get('FL33T_SESSION_TOKEN')

    key = '--'.join((team_id, session_token))
    if key not in clients:
        try:
            clients[key] = Fl33tClient(team_id, session_token)
        except ValueError:
            click.echo('ERROR: You must either pass --team-id and --session-token or have')
            click.echo('FL33T_TEAM_ID and FL33T_SESSION_TOKEN set in your environment.')
            raise

    return clients[key]


@click.group()
@click.option('--team-id', type=str)
@click.option('--session-token', type=str)
@click.pass_context
def cli(ctx, team_id=None, session_token=None):
    """Commands to interact with the Fl33t API directly"""

    ctx.ensure_object(dict)
    ctx.obj['get_fl33t_client'] = lambda: create_client(team_id, session_token)


cli.add_command(fleets_cmds, name='fleets')
cli.add_command(trains_cmds, name='trains')

if __name__ == "__main__":
    cli()