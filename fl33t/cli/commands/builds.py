"""
fl33t.cli.commands.builds

Command line interaction for Fl33t builds
"""

import click


@click.group()
def cli():
    """Commands to interact with the Fl33t builds"""
    pass


@cli.command()
@click.option('-t', '--show-train', is_flag=True, default=False)
@click.pass_context
def list(ctx, show_train):
    """Show information about all builds"""

    for build in ctx.obj['get_fl33t_client']().list_builds():
        click.echo(build)

        if show_train:
            click.echo('Train:')
            click.echo('    - {}'.format(build.train))


@cli.command()
@click.argument('build_id')
@click.option('-t', '--show-train', is_flag=True, default=False)
@click.pass_context
def show(ctx, build_id, show_train):
    """Show information about a single build"""

    build = ctx.obj['get_fl33t_client']().get_build(build_id)
    click.echo(build)

    if show_train:
        click.echo('Train:')
        click.echo('    - {}'.format(build.train))


@cli.command()
@click.argument('build_id')
@click.pass_context
def delete(ctx, build_id):
    """Delete a build from Fl33t"""

    build = ctx.obj['get_fl33t_client']().get_build(build_id)
    if not build:
        click.echo('Build does not exist in Fl33t. Cannot proceed with '
                   'deletion.')
        return

    if build.delete():
        click.echo('Build was deleted.')
    else:
        click.echo('Build failed to be deleted.')


@cli.command()
@click.argument('filename')
@click.option('-v', '--version', prompt=True, type=str)
@click.option('-t', '--train-id', prompt=True, type=str)
@click.option('-r/-u', '--released/--unreleased', is_flag=True, default=False)
@click.option('-s', '--md5sum', default=None)
@click.pass_context
def create(ctx, filename, version, train_id, released, md5sum):
    """Add a build to Fl33t"""

    build = ctx.obj['get_fl33t_client']().Build(
        filename=filename,
        version=version,
        train_id=train_id,
        released=released,
        md5sum=md5sum,
    )

    if build.create():
        click.echo('Build was created.')
    else:
        click.echo('Build failed to be created.')


@cli.command()
@click.argument('build_id')
@click.option('-r/-u', '--released/--unreleased', is_flag=True, prompt=True)
@click.pass_context
def update(ctx, build_id, released):
    """Update a build in Fl33t"""

    build = ctx.obj['get_fl33t_client']().get_build(build_id)
    if not build:
        click.echo('Build does not exist in Fl33t. Cannot proceed with '
                   'modification.')
        return

    if build.released != released:
        build.released = released

        if build.update():
            click.echo('Build has been updated.')
        else:
            click.echo('Build failed to be updated.')

    else:
        click.echo('Build is already in sync with desired changes.')
