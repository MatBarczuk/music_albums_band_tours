import re

import click
from flask import current_app
from flask.cli import with_appcontext

from app.extentions import db
from app.auth.models import User


@click.command('list_bp_endpoints')
@click.argument('blueprint')
@with_appcontext
def list_bp_endpoints(blueprint):
    for endpoint in current_app.view_functions.keys():
        if re.search(f'^{blueprint}.', endpoint):
            click.echo(endpoint)


@click.group('user')
def user():
    pass


@user.command('create')
@click.option('-u', '--username', prompt='Username', help='Users username', required=True)
@click.option('-e', '--email', prompt='Email', help='Users email', required=True)
@click.option('-p', '--password', prompt='Password', help='Users password', required=True, hide_input=True,
              default='password123')
@click.option('-a', '--admin', prompt='Is this user an admin', help='It turns the new user int an admin', is_flag=True)
@with_appcontext
def create(username, email, password, admin):
    user = User.query.filter_by(username=username).first()
    if user:
        click.echo('User already exists with that username, please choose another username.')
        return

    user = User.query.filter_by(email=email).first()
    if user:
        click.echo('User with that email already exists, please choose another email.')

    user = User(username, email, password)
    if admin:
        user.make_admin()

    try:
        db.session.add(user)
        db.session.commit()
        click.echo(f'User {user.username} has been successfully created.')
    except Exception as e:
        click.echo('Something went wrong')
        click.echo(e)
        db.session.rollback()


def register_click_commands(app):
    app.cli.add_command(list_bp_endpoints)
    app.cli.add_command(user)
