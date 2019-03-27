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
@click.option('--show-fleet/--no-show-fleet', is_flag=True, default=False)
@click.option('--show-builds/--no-show-builds', is_flag=True, default=False)
@click.pass_context
def list(ctx, show_fleet, show_builds):
    """Show information about all fleets"""

    for train in ctx.obj['get_fl33t_client']().list_trains():
        print(train)
        if show_fleet:
            print(train.fleet)

        if show_builds:
            for build in train.builds():
                print(build)


@cli.command()
@click.argument('train_id')
@click.option('--show-fleet/--no-show-fleet', is_flag=True, default=False)
@click.option('--show-builds/--no-show-builds', is_flag=True, default=False)
@click.pass_context
def show(ctx, train_id, show_fleet, show_builds):
    """Show information about a single fleet"""

    train = ctx.obj['get_fl33t_client']().get_train(train_id)
    print(train)
    if show_fleet:
        print(train.fleet)

    if show_builds:
        for build in train.builds():
            print(build)