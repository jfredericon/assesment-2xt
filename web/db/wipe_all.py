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
                                      port=DATABASE_PORT)

        connection.autocommit = True
        cursor = connection.cursor()
        delete_database_query = f'DROP DATABASE {DATABASE_NAME}'
        cursor.execute(delete_database_query)

    except (Exception) as error:
        raise Exception(f'Error while erase all database \n{str(error)}')
    finally:
        if(connection):
            cursor.close()
            connection.close()


if __name__ == '__main__':
    run()
