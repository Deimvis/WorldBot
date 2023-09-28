import logging
import os
from psycopg2.extensions import AsIs
from src.utils.postgres import PostgresConnection, create_database, drop_database

def init_db():
    with PostgresConnection(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
            ) as conn:
        create_database(conn, os.getenv('DB_NAME'), if_not_exists=True)

    with PostgresConnection(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                db_name=os.getenv('DB_NAME'),
            ) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS %s (
                        id BIGSERIAL PRIMARY KEY,
                        text TEXT,
                        author VARCHAR(255) DEFAULT '—'::varchar,
                        UNIQUE(author, text)
                    )
                """,
                (AsIs("quote"),)
            )
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS %s (
                        id BIGSERIAL PRIMARY KEY,
                        chat_id VARCHAR(255),
                        name VARCHAR(255),
                        type VARCHAR(255),
                        value VARCHAR(255)
                    )
                """,
                (AsIs("quotes_subscription"),)
            )
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS %s (
                        chat_id BIGINT PRIMARY KEY,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT
                    )
                """,
                (AsIs("user"),)
            )
    logging.debug('Database "{}" has been initialized'.format(os.getenv('DB_NAME')))


def drop_db():
    with PostgresConnection(
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
            ) as conn:
        drop_database(conn, os.getenv('DB_NAME'))
