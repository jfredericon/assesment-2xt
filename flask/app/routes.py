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

        cursor = connection.cursor()
        connection.autocommit = True

        more_distant = None

        sql = f"SELECT F.departure_airport, F. arrival_airport, FM.distance \
                FROM flight AS F \
                INNER JOIN flight_metrics AS FM \
                ON F.id = FM.flight_id \
                ORDER BY FM.distance DESC \
                LIMIT 30;"
        cursor.execute(sql)

        more_distant = cursor.fetchall()

        longer_duration = None

        sql = f"SELECT F.departure_airport, F. arrival_airport, \
                (arrival_time - departure_time) AS flight_time, \
                AC.aircraft_manufacturer, AC.aircraft_model \
                FROM flight AS F \
                INNER JOIN aircraft AS AC \
                ON F.aircraft_id = AC.id \
                ORDER BY flight_time DESC \
                LIMIT 30;"
        cursor.execute(sql)

        longer_duration = cursor.fetchall()

        state_with_more_airports = None

        sql = f"SELECT state, COUNT(id) AS quant FROM airport \
                GROUP BY state \
                ORDER BY quant DESC \
                LIMIT 1;"
        cursor.execute(sql)

        state_with_more_airports = cursor.fetchone()

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
