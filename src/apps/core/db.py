import telebot
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


USER_TABLE = PostgresTable(connection, 'user')


def update_user_info(user: telebot.types.User):
    if not USER_TABLE.has(where={'id': user.id}):
        USER_TABLE.insert([{
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }])
        USER_TABLE.commit()
