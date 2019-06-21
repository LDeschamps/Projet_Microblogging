from flask import Flask
from models import *
from faker import Factory
import click
app = Flask(__name__)


@app.cli.command()
def initdb():
    """Create database"""
    create_tables()
    click.echo('Initialized the database')

@app.cli.command()
def dropdb():
    """Drop database tables"""
    drop_tables()
    click.echo('Dropped tables from database')

@app.cli.command()
def fakedata():
    fake = Factory.create()
    for pk in range(0, 10):
        User.create(username=fake.first_name(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.email(),
                    password=fake.password())