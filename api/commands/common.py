# -*- coding: utf-8 -*-
"""Click commands."""


import click
from flask.cli import with_appcontext
from api.extensions import db




@click.command()
@with_appcontext
def db_setup():
    """create tables
    """
    db.create_all()

# @click.command()
# @with_appcontext
# def db():
#     manager.add_command('db', MigrateCommand)