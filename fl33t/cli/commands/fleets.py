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
@click.option('--show-train/--no-show-train', is_flag=True, default=False)
@click.option('--show-builds/--no-show-builds', is_flag=True, default=False)
@click.option('--list-devices/--no-list-devices', is_flag=True, default=False)
@click.pass_context
def list(ctx, show_train, show_builds, list_devices):
    """Show information about all fleets"""

    for fleet in ctx.obj['get_fl33t_client']().list_fleets():
        print(fleet)
        if show_train:
            print(fleet.train)

        if show_builds:
            for build in fleet.train.builds():
                print(build)

        if list_devices:
            for device in fleet.devices():
                print(device)


@cli.command()
@click.argument('fleet_id')
@click.option('--show-train/--no-show-train', is_flag=True, default=False)
@click.option('--show-builds/--no-show-builds', is_flag=True, default=False)
@click.option('--list-devices/--no-list-devices', is_flag=True, default=False)
@click.pass_context
def show(ctx, fleet_id, show_train, show_builds, list_devices):
    """Show information about a single fleet"""

    fleet = ctx.obj['get_fl33t_client']().get_fleet(fleet_id)
    print(fleet)
    if show_train:
        print(fleet.train)

    if show_builds:
        for build in fleet.train.builds():
            print(build)

    if list_devices:
        for device in fleet.devices():
            print(device)
