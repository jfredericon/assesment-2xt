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
    more_distant = None
    longer_duration = None
    state_with_more_airports = None
    departure_airports = None

    try:
        connection = psycopg2.connect(user=DATABASE_USER,
                                    password=DATABASE_PASSWORD,
                                    host=DATABASE_HOST,
                                    port=DATABASE_PORT,
                                    database=DATABASE_NAME)

        cursor = connection.cursor()
        connection.autocommit = True

        sql = f"SELECT departure_airport, arrival_airport, REPLACE(ROUND(distance::numeric, 2)::text, '.', ',') AS distance \
                FROM flight \
                ORDER BY distance DESC \
                LIMIT 30;"
        cursor.execute(sql)

        more_distant = cursor.fetchall()

        sql = f"SELECT F.departure_airport, F. arrival_airport, \
                TO_CHAR((arrival_time - departure_time), 'HH24:MI') AS flight_time, \
                AC.aircraft_model, AC.aircraft_manufacturer \
                FROM flight AS F \
                INNER JOIN flight_metrics AS FM \
                ON F.id = FM.flight_id \
                INNER JOIN aircraft AS AC \
                ON FM.aircraft_id = AC.id \
                ORDER BY flight_time DESC \
                LIMIT 30;"
        cursor.execute(sql)

        longer_duration = cursor.fetchall()

        sql = f"SELECT state, COUNT(id) AS quant FROM airport \
                GROUP BY state \
                ORDER BY quant DESC \
                LIMIT 1;"
        cursor.execute(sql)

        state_with_more_airports = cursor.fetchone()

        sql = f"SELECT FMIN.departure_airport, \
                FMAX.arrival_airport AS arrival_airport_max, REPLACE(ROUND(FMAX.distance::numeric, 2)::text, '.', ',') AS max_distance, \
                FMIN.arrival_airport AS arrival_airport_min, REPLACE(ROUND(FMIN.distance::numeric, 2)::text, '.', ',') AS min_distance  \
                FROM ( \
                SELECT DISTINCT ON (departure_airport) departure_airport, arrival_airport, MAX(distance) AS distance \
                FROM flight \
                GROUP BY departure_airport, arrival_airport \
                ORDER BY departure_airport ASC, distance DESC \
                ) AS FMAX \
                INNER JOIN \
                ( \
                SELECT DISTINCT ON (departure_airport) departure_airport, arrival_airport, MIN(distance) AS distance \
                FROM flight \
                GROUP BY departure_airport, arrival_airport \
                ORDER BY departure_airport ASC, distance ASC \
                ) AS FMIN \
                ON FMAX.departure_airport = FMIN.departure_airport;"
        cursor.execute(sql)

        departure_airports = cursor.fetchall()

    except (Exception) as error:
        click.secho(str(error), fg='red')
        sys.exit()
    finally:
        if(connection):
            connection.close()
        else:
            raise Exception(
                f'Error while connect database')

    return render_template('index.html',
                        more_distant=more_distant, 
                        longer_duration=longer_duration, 
                        state_with_more_airports=state_with_more_airports, 
                        departure_airports=departure_airports)
