import psycopg2
from psycopg2.extensions import AsIs
from lib.utils.temporary import temp_setattr


class PostgresConnection:
    def __init__(self, db_name=None, user=None, password=None, host=None, port=None):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def __enter__(self):
        self.conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()


def create_database(conn: psycopg2.extensions.connection, db_name: str, if_not_exists=False) -> bool:
    query = """
        CREATE DATABASE %s
            ENCODING='UTF8'
            LC_COLLATE='C'
            LC_CTYPE='C'
            TEMPLATE template0
    """
    already_exists = False
    with temp_setattr(conn, 'autocommit', True):
        with conn.cursor() as cursor:
            try:
                cursor.execute(query, (AsIs(db_name),))
            except psycopg2.errors.DuplicateDatabase:
                if not if_not_exists:
                    raise
                already_exists = True
    return not already_exists


def drop_database(conn: psycopg2.extensions.connection, db_name: str):
    with conn.cursor() as cursor:
        cursor.execute('DROP DATABASE IF EXISTS %s', (AsIs(db_name),))
