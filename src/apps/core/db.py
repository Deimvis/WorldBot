import os
import psycopg2
from lib.storages.postgres import PostgresTable


connection = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    dbname=os.getenv('DB_NAME'),
)


USER_TABLE = PostgresTable(connection, 'users')
