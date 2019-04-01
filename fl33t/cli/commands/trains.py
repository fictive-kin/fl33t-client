"""
fl33t.cli.commands.trains

Command line interaction for Fl33t trains
"""

import click


@click.group()
def cli():
    """Commands to interact with the Fl33t trains"""
    pass


@cli.command()
@click.option('-f', '--show-fleet', is_flag=True, default=False)
@click.option('-b', '--list-builds', is_flag=True, default=False)
@click.pass_context
def list(ctx, show_fleet, list_builds):
    """Show information about all fleets"""

    for train in ctx.obj['get_fl33t_client']().list_trains():
        click.echo(train)
        if show_fleet:
            click.echo('Train:')
            click.echo('    - {}'.format(train.fleet))

        if list_builds:
            click.echo('Builds:')
            for build in train.builds():
                click.echo('    - {}'.format(build))


@cli.command()
@click.argument('train_id')
@click.option('-f', '--show-fleet', is_flag=True, default=False)
@click.option('-b', '--list-builds', is_flag=True, default=False)
@click.pass_context
def show(ctx, train_id, show_fleet, list_builds):
    """Show information about a single fleet"""

    train = ctx.obj['get_fl33t_client']().get_train(train_id)
    click.echo(train)
    if show_fleet:
        click.echo('Train:')
        click.echo('    - {}'.format(train.fleet))

    if list_builds:
        click.echo('Builds:')
        for build in train.builds():
            click.echo('    - {}'.format(build))


@cli.command()
@click.argument('train_id')
@click.pass_context
def delete(ctx, train_id):
    """Delete a train from Fl33t"""

    train = ctx.obj['get_fl33t_client']().get_train(train_id)
    if not train:
        click.echo('Train does not exist in Fl33t. Cannot proceed with '
                   'deletion.')
        return

    if train.delete():
        click.echo('Train was deleted.')
    else:
        click.echo('Train failed to be deleted.')


@cli.command()
@click.argument('name')
@click.pass_context
def create(ctx, name):
    """Add a train to Fl33t"""

    train = ctx.obj['get_fl33t_client']().Train(
        name=name,
    )

    if train.create():
        click.echo('Train was created.')
    else:
        click.echo('Train failed to be created.')


@cli.command()
@click.argument('train_id')
@click.option('-n', '--name', type=str, default=None)
@click.pass_context
def update(ctx, train_id, name):
    """Update a train in Fl33t"""

    train = ctx.obj['get_fl33t_client']().get_train(train_id)
    if not train:
        click.echo('Train does not exist in Fl33t. Cannot proceed with '
                   'modification.')
        return

    if name and train.name != name:
        train.name = name

        if train.update():
            click.echo('Train has been updated.')
        else:
            click.echo('Train failed to be updated.')
    else:
        click.echo('Train is already in sync with desired changes.')
