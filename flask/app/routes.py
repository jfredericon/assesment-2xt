from flask import url_for, render_template
from app import app
import psycopg2
import click
import sys
import os

DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_PORT = os.environ.get('DATABASE_PORT')
DATABASE_NAME = os.environ.get('DATABASE_NAME')


@app.route("/")
def index():
    connection = None
    try:
        connection = psycopg2.connect(user=DATABASE_USER,
                                    password=DATABASE_PASSWORD,
                                    host=DATABASE_HOST,
                                    port=DATABASE_PORT,
                                    database=DATABASE_NAME)

    except (Exception) as error:
        click.secho(str(error), fg='red')
        sys.exit()
    finally:
        if(connection):
            connection.close()
        else:
            raise Exception(
                f'Error while connect database')


    return render_template('index.html')