from flask import Flask, render_template, url_for, request
from models import *
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
    from faker import Faker
    fake = Faker()
    for pk in range(0, 10):
        User.create(username=fake.username(), 
                        firstname=fake.first_name(),
                        last_name=fake.last_name(),
                        email=fake.email(),
                        password=fake.password())