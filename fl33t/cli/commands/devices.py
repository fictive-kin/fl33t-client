"""
fl33t.cli.commands.devices

Command line interaction for Fl33t devices
"""

import click


@click.group()
def cli():
    """Commands to interact with the Fl33t devices"""
    pass


@cli.command()
@click.option('-t', '--show-train', is_flag=True, default=False)
@click.option('-b', '--show-build', is_flag=True, default=False)
@click.pass_context
def list(ctx, show_train, show_build):
    """Show information about all devices"""

    for device in ctx.obj['get_fl33t_client']().list_devices():
        click.echo(device)

        if show_train:
            click.echo('Train:')
            click.echo('    - {}'.format(device.train))

        if show_build:
            click.echo('Build:')
            click.echo('    - {}'.format(device.build))


@cli.command()
@click.argument('device_id')
@click.option('-t', '--show-train', is_flag=True, default=False)
@click.option('-b', '--show-build', is_flag=True, default=False)
@click.pass_context
def show(ctx, device_id, show_train, show_build):
    """Show information about a single device"""

    device = ctx.obj['get_fl33t_client']().get_device(device_id)
    click.echo(device)

    if show_train:
        click.echo('Train:')
        click.echo('    - {}'.format(device.train))

    if show_build:
        click.echo('Build:')
        click.echo(device.build)


@cli.command()
@click.argument('device_id')
@click.pass_context
def delete(ctx, device_id):
    """Delete a device from Fl33t"""

    device = ctx.obj['get_fl33t_client']().get_device(device_id)
    if not device:
        click.echo('Device does not exist in Fl33t. Cannot proceed with '
                   'deletion.')
        return

    if device.delete():
        click.echo('Device was deleted.')
    else:
        click.echo('Device failed to be deleted.')


@cli.command()
@click.argument('device_id')
@click.option('-f', '--fleet_id', prompt=True)
@click.option('-n', '--name', prompt=True)
@click.pass_context
def create(ctx, device_id, fleet_id, name):
    """Add a device to Fl33t"""

    device = ctx.obj['get_fl33t_client']().get_device(device_id)
    if device:
        click.echo('Device already exists in Fl33t. Cannot proceed with '
                   'creation.')
        click.echo(device)
        return

    device = ctx.obj['get_fl33t_client']().Device(
        device_id=device_id,
        fleet_id=fleet_id,
        name=name,
    )

    if device.create():
        click.echo('Device was created.')
    else:
        click.echo('Device failed to be created.')


@cli.command()
@click.argument('device_id')
@click.option('-f', '--fleet-id', default=None)
@click.option('-n', '--name', default=None)
@click.pass_context
def update(ctx, device_id, fleet_id, name):
    """Update a device in Fl33t"""

    device = ctx.obj['get_fl33t_client']().get_device(device_id)
    if not device:
        click.echo('Device does not exist in Fl33t. Cannot proceed with '
                   'modification.')
        return

    changes = False

    if fleet_id and device.fleet_id != fleet_id:
        device.fleet_id = fleet_id
        changes = True

    if name and device.name != name:
        device.name = name
        changes = True

    if changes:
        if device.update():
            click.echo('Device has been updated.')
        else:
            click.echo('Device failed to be updated.')
    else:
        click.echo('Device is already in sync with desired changes.')
