import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')

def run():
    connection = None
    try:
        connection = psycopg2.connect(user=DATABASE_USER,
                                      password=DATABASE_PASSWORD,
                                      host=DATABASE_HOST,
                                      port=DATABASE_PORT,
                                      database=DATABASE_NAME)

        cursor = connection.cursor()
        create_table_query = [
            '''
            CREATE TABLE IF NOT EXISTS airport
            (
                id SERIAL PRIMARY KEY,
                iata VARCHAR(3) NOT NULL UNIQUE,
                city VARCHAR NOT NULL,
                state VARCHAR(2) NOT NULL,
                lat FLOAT8 NOT NULL,
                long FLOAT8 NOT NULL,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            );
        ''',
            '''
            CREATE TABLE IF NOT EXISTS flight
            (
                id SERIAL PRIMARY KEY,
                airport_from VARCHAR(3) NOT NULL
                 REFERENCES airport(iata),
                airport_to VARCHAR(3) NOT NULL
                 REFERENCES airport(iata),
                aircraft_id VARCHAR NOT NULL,
                departure_date DATE NOT NULL,
                departure_time TIMESTAMP NOT NULL,
                arrival_time TIMESTAMP NOT NULL,
                farel_price DOUBLE PRECISION NOT NULL,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            );
        ''',
            '''
            CREATE TABLE IF NOT EXISTS aircraft
            (
                id SERIAL PRIMARY KEY,
                aircraft_model VARCHAR NOT NULL,
                aircraft_manufacturer VARCHAR NOT NULL,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            );
        ''',
            '''
            CREATE TABLE IF NOT EXISTS flight_metrics
            (
                id SERIAL PRIMARY KEY,
                flight_id INTEGER NOT NULL
                 REFERENCES flight(id),
                url_api TEXT NOT NULL,
                distance DOUBLE PRECISION NOT NULL,
                low_value VARCHAR NOT NULL,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            );
        ''']

        for query in create_table_query:
            cursor.execute(query)

        connection.commit()

    except (Exception) as error:
        raise Exception(f'Error while creating table \n{str(error)}')
    finally:
        if(connection):
            cursor.close()
            connection.close()
        else:
            raise Exception(
                f'Error while connect database')


if __name__ == "__main__":
    run()
