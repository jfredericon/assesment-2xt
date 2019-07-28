from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')


def run():
    connection = None
    print(DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME)
    try:
        connection = psycopg2.connect(user=DATABASE_USER,
                                      password=DATABASE_PASSWORD,
                                      host=DATABASE_HOST,
                                      port=DATABASE_PORT)

        connection.autocommit = True
        cursor = connection.cursor()
        create_database_query = f'CREATE DATABASE {DATABASE_NAME}'
        cursor.execute(create_database_query)

    except (Exception) as error:
        raise Exception(
            f'Error while create database \n{str(error)}')
    finally:
        if(connection):
            cursor.close()
            connection.close()


if __name__ == "__main__":
    run()
