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
        truncate_table_query = [
            f'TRUNCATE TABLE aircraft',
            f'TRUNCATE TABLE flight_metrics',
            f'TRUNCATE TABLE flight CASCADE',
            f'TRUNCATE TABLE airport Cascade'
        ]

        for query in truncate_table_query:
            cursor.execute(query)

        connection.commit()

    except (Exception) as error:
        raise Exception(f'Error while erase data \n{str(error)}')
    finally:
        if(connection):
            cursor.close()
            connection.close()


if __name__ == '__main__':
    run()
