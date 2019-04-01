"""
fl33t.cli.commands.sessions

Command line interaction for Fl33t sessions
"""

import click


TYPES = [
    'account',
    'api',
    'device',
]
PRIVILEGES = [
    'admin',
    'device',
    'provisioning',
    'readonly',
    'upload',
]


@click.group()
def cli():
    """Commands to interact with the Fl33t sessions"""
    pass


@cli.command()
@click.pass_context
def list(ctx):
    """Show information about all sessions"""

    for session in ctx.obj['get_fl33t_client']().list_sessions():
        click.echo(session)


@cli.command()
@click.argument('session_token')
@click.pass_context
def show(ctx, session_token):
    """Show information about a single session"""

    session = ctx.obj['get_fl33t_client']().get_session(session_token)
    click.echo(session)


@cli.command()
@click.argument('session_token')
@click.pass_context
def delete(ctx, session_token):
    """Delete a session from Fl33t"""

    session = ctx.obj['get_fl33t_client']().get_session(session_token)
    if not session:
        click.echo('Session does not exist in Fl33t. Cannot proceed with '
                   'deletion.')
        return

    if session.delete():
        click.echo('Session was deleted.')
    else:
        click.echo('Session failed to be deleted.')


@cli.command()
@click.option('-p', '--privilege', type=click.Choice(PRIVILEGES), prompt=True)
@click.option('-t', '--type', 'type_', type=click.Choice(TYPES), default='api')
@click.pass_context
def create(ctx, privilege, type_):
    """Add a session to Fl33t"""

    session = ctx.obj['get_fl33t_client']().Session(
        type=type_
    )
    setattr(session, privilege, True)

    if session.create():
        click.echo('Session was created.')
    else:
        click.echo('Session failed to be created.')


@cli.command()
@click.argument('session_token')
@click.option('-p', '--privilege', type=click.Choice(PRIVILEGES), prompt=True)
@click.pass_context
def update(ctx, session_token, privilege):
    """Update a session in Fl33t"""

    session = ctx.obj['get_fl33t_client']().get_session(session_token)
    if not session:
        click.echo('Session does not exist in Fl33t. Cannot proceed with '
                   'modification.')
        return

    if session.priv != privilege:
        for priv in PRIVILEGES:
            setattr(session, priv, (priv == privilege))

        if session.update():
            click.echo('Session has been updated.')
        else:
            click.echo('Session failed to be updated.')
    else:
        click.echo('Session is already in sync with desired changes.')
