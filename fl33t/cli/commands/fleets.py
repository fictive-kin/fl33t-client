"""
fl33t.cli.commands.fleets

Command line interaction for Fl33t fleets
"""

import click


@click.group()
def cli():
    """Commands to interact with the Fl33t fleets"""
    pass


@cli.command()
@click.option('-t', '--show-train', is_flag=True, default=False)
@click.option('-b', '--list-builds', is_flag=True, default=False)
@click.option('-d', '--list-devices', is_flag=True, default=False)
@click.pass_context
def list(ctx, show_train, list_builds, list_devices):
    """Show information about all fleets"""

    for fleet in ctx.obj['get_fl33t_client']().list_fleets():
        click.echo(fleet)
        if show_train:
            click.echo('Train:')
            click.echo('    - {}'.format(fleet.train))

        if list_builds:
            click.echo('Builds:')
            for build in fleet.train.builds():
                click.echo('    - {}'.format(build))

        if list_devices:
            click.echo('Devices:')
            for device in fleet.devices():
                click.echo('    - {}'.format(device))


@cli.command()
@click.argument('fleet_id')
@click.option('-t', '--show-train', is_flag=True, default=False)
@click.option('-b', '--list-builds', is_flag=True, default=False)
@click.option('-d', '--list-devices', is_flag=True, default=False)
@click.pass_context
def show(ctx, fleet_id, show_train, list_builds, list_devices):
    """Show information about a single fleet"""

    fleet = ctx.obj['get_fl33t_client']().get_fleet(fleet_id)
    click.echo(fleet)
    if show_train:
        click.echo('Train:')
        click.echo('    - {}'.format(fleet.train))

    if list_builds:
        click.echo('Builds:')
        for build in fleet.train.builds():
            click.echo('    - {}'.format(build))

    if list_devices:
        click.echo('Devices:')
        for device in fleet.devices():
            click.echo('    - {}'.format(device))


@cli.command()
@click.argument('fleet_id')
@click.pass_context
def delete(ctx, fleet_id):
    """Delete a fleet from Fl33t"""

    fleet = ctx.obj['get_fl33t_client']().get_fleet(fleet_id)
    if not fleet:
        click.echo('Fleet does not exist in Fl33t. Cannot proceed with '
                   'deletion.')
        return

    if fleet.delete():
        click.echo('Fleet was deleted.')
    else:
        click.echo('Fleet failed to be deleted.')


@cli.command()
@click.argument('name')
@click.option('-t', '--train-id', prompt=True, type=str)
@click.option('-b', '--build-id', prompt=True, type=str)
@click.option('-u/-r', '--unreleased/--only-released', default=False)
@click.pass_context
def create(ctx, name, train_id, build_id, unreleased):
    """Add a fleet to Fl33t"""

    fleet = ctx.obj['get_fl33t_client']().Fleet(
        name=name,
        train_id=train_id,
        build_id=build_id,
        unreleased=unreleased,
    )

    if fleet.create():
        click.echo('Fleet was created.')
    else:
        click.echo('Fleet failed to be created.')


@cli.command()
@click.argument('fleet_id')
@click.option('-n', '--name', type=str, default=None)
@click.option('-t', '--train-id', type=str, default=None)
@click.option('-b', '--build-id', type=str, default=None)
@click.option('-u/-r', '--unreleased/--only-released', default=False)
@click.pass_context
def update(ctx, fleet_id, name, train_id, build_id, unreleased):
    """Update a fleet in Fl33t"""

    fleet = ctx.obj['get_fl33t_client']().get_fleet(fleet_id)
    if not fleet:
        click.echo('Fleet does not exist in Fl33t. Cannot proceed with '
                   'modification.')
        return

    changes = False

    if name and fleet.name != name:
        fleet.name = name
        changes = True

    if train_id and fleet.train_id != train_id:
        fleet.train_id = train_id
        changes = True

    if build_id and fleet.build_id != build_id:
        fleet.build_id = build_id
        changes = True

    if fleet.unreleased != unreleased:
        fleet.unreleased = unreleased
        changes = True

    if changes:
        if fleet.update():
            click.echo('Fleet has been updated.')
        else:
            click.echo('Fleet failed to be updated.')
    else:
        click.echo('Fleet is already in sync with desired changes.')
