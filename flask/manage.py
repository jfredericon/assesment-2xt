from db import create_database, create_table, wipe_data, wipe_all
from datetime import datetime, timedelta
from utils import operations
from decimal import Decimal
from data import air
import psycopg2
import click
import sys
import os

DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')


@click.group()
def main():
    pass


@main.command('migrate', help='Create database and tables')
def migrate():
    try:
        click.echo('-> Creating database...')
        create_database.run()
        click.secho('-> Database created successfully!', fg='green')
    except (Exception) as error:
        click.secho(str(error), fg='red')
        sys.exit()

    try:
        click.echo('-> Creating tables...')
        create_table.run()
        click.secho('-> Tables created successfully!', fg='green')
    except (Exception) as error:
        click.secho(str(error), fg='red')
        sys.exit()


@main.command('wipe-data', help='Erase all data')
def wipedata():
    try:
        click.echo('-> Erase all data...')
        wipe_data.run()
        click.secho('-> Erase all data successfully!', fg="green")
    except (Exception) as error:
        click.secho(str(error), fg="red")
        sys.exit()


@main.command('wipe-all', help='Erase all database')
def wipeall():
    try:
        click.echo('-> Erase all database...')
        wipe_all.run()
        click.secho('-> Erase all database successfully!', fg='green')
    except (Exception) as error:
        click.secho(str(error), fg='red')
        sys.exit()


@main.command('data-only', help='Get data')
def dataonly():
    connection = None
    try:
        connection = psycopg2.connect(user=DATABASE_USER,
                                      password=DATABASE_PASSWORD,
                                      host=DATABASE_HOST,
                                      port=DATABASE_PORT,
                                      database=DATABASE_NAME)

        cursor = connection.cursor()
        connection.autocommit = True
        click.echo('-> Get airports data...')
        airports = air.airports()

        for airport in airports.values():
            sql = f"SELECT id FROM airport WHERE iata = '{airport['iata']}'"
            cursor.execute(sql)

            if(cursor.fetchone() is None):
                sql = f"INSERT INTO airport (iata, city, state, lat, long, created_at, updated_at )\
                        VALUES (\
                    '{airport['iata']}',\
                    '{airport['city']}',\
                    '{airport['state']}',\
                    {airport['lat']},\
                    {airport['lon']},\
                    CURRENT_TIMESTAMP,\
                    CURRENT_TIMESTAMP\
                )"
                cursor.execute(sql)

        click.secho('-> Get airports data successfully!', fg='green')

        click.echo('-> Generated airports combine...')
        comb = air.combine(airports.keys())
        total_comb = len(comb)
        click.secho('-> Generated airports combine successfully!', fg='green')

        click.echo('-> Proccessing metrics')
        departure_date = datetime.now() + timedelta(days=40)

        # comb = comb[:20]
        sql = f"SELECT  departure_airport, arrival_airport FROM flight \
            WHERE date(departure_time) = '{departure_date:%Y-%m-%d}' \
            ORDER BY date(departure_time) DESC, id DESC LIMIT 1"

        cursor.execute(sql)
        flight = cursor.fetchone()
        increment_current = 1
        if(flight is not None):
            if(flight in comb):
                index = comb.index(flight) + 1
                comb = comb[index:]
                # total_comb = len(comb)
                increment_current += index

        for item in comb:
            current = comb.index(item) + increment_current

            click.secho(f'[... {current} in {total_comb} ...]')

            departure_airport = item[0]
            arrival_airport = item[1]

            resp = air.search(departure_airport, arrival_airport,
                              departure_date)

            from_city = resp['data']['summary']['from']
            to_city = resp['data']['summary']['to']

            lon1 = from_city['lon']
            lat1 = from_city['lat']
            lon2 = to_city['lon']
            lat2 = to_city['lat']

            distance = operations.haversine(lon1, lat1, lon2, lat2)

            sorted_list_aircrafts = sorted(
                resp['data']['options'], key=lambda item: item['fare_price']
            )

            for model in sorted_list_aircrafts:
                sql = f"SELECT id FROM aircraft \
                    WHERE aircraft_model = \
                    '{model['aircraft']['model']}' \
                    AND aircraft_manufacturer = \
                    '{model['aircraft']['manufacturer']}'"

                cursor.execute(sql)
                aircraft_id = cursor.fetchone()

                if(aircraft_id is not None):
                    aircraft_id = aircraft_id[0]
                else:
                    sql = f"INSERT INTO aircraft \
                        (aircraft_model, aircraft_manufacturer, created_at, \
                        updated_at) VALUES( \
                        '{model['aircraft']['model']}', \
                        '{model['aircraft']['manufacturer']}',\
                        CURRENT_TIMESTAMP, \
                        CURRENT_TIMESTAMP \
                    ) RETURNING id"

                    cursor.execute(sql)
                    aircraft_id = cursor.fetchone()
                    if(aircraft_id is not None):
                        aircraft_id = aircraft_id[0]

                sql = f"SELECT id FROM flight\
                    WHERE departure_airport = '{departure_airport}' \
                    AND arrival_airport = '{arrival_airport}' \
                    AND departure_time = '{model['departure_time']}' \
                    AND aircraft_id = '{aircraft_id}'"

                cursor.execute(sql)
                flight_id = cursor.fetchone()

                if(flight_id is None):
                    departure_time = datetime.strptime(
                        model['departure_time'], '%Y-%m-%dT%H:%M:%S'
                    )

                    arrival_time = datetime.strptime(
                        model['arrival_time'], '%Y-%m-%dT%H:%M:%S'
                    )

                    flight_time_decimal = operations.flight_time(
                        departure_time, arrival_time)

                    average_speed = operations.average_speed(
                        distance, flight_time_decimal)

                    fare_price = model['fare_price']

                    price_per_km = operations.price_per_km(
                        fare_price, distance)

                    sql = f"INSERT INTO flight \
                        (departure_airport, \
                        arrival_airport, \
                        aircraft_id, \
                        departure_time, \
                        arrival_time, \
                        fare_price, \
                        average_speed,\
                        price_per_km, \
                        created_at, updated_at) \
                        VALUES('{departure_airport}', \
                            '{arrival_airport}', \
                            '{aircraft_id}', \
                            '{model['departure_time']}', \
                            '{model['arrival_time']}', \
                            {model['fare_price']}, \
                            {average_speed}, \
                            {price_per_km}, \
                            CURRENT_TIMESTAMP, \
                            CURRENT_TIMESTAMP) RETURNING id"

                    cursor.execute(sql)
                    flight_id = cursor.fetchone()

                    if(flight_id is not None):
                        flight_id = flight_id[0]

                        if(sorted_list_aircrafts.index(model) == 0):
                            sql = f"INSERT INTO flight_metrics\
                                (flight_id, url_api, distance, \
                                lowest_value, created_at, updated_at) \
                                VALUES ('{flight_id}', '{resp['url']}', \
                                '{distance}', '{fare_price}', \
                                CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"

                            cursor.execute(sql)

                        # print(
                        #     {
                        #         'from': from_city['city'],
                        #         'to': to_city['city'],
                        #         'distance': f'{distance:.2f} km',
                        #         'departure_time': f'{departure_time:%d-%m-%Y %H:%M:%S}',
                        #         'arrival_time': f'{arrival_time:%d-%m-%Y %H:%M:%S}',
                        #         'flight_time': f'{flight_time:.2f} h',
                        #         'average_speed': f'{average_speed:.2f} km/h',
                        #         'fare_price': f'R$ {fare_price}',
                        #         'price_per_km': f'R$ {price_per_km:.2f}'
                        #     }
                        # )

        click.secho('-> Proccessing metrics successfully!', fg='green')
    except (Exception) as error:
        click.secho(str(error), fg='red')
        sys.exit()
    finally:
        if(connection):
            cursor.close()
            connection.close()
        else:
            raise Exception(
                f'Error while connect database')


if __name__ == "__main__":
    main()
