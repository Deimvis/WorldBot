from lib.storages.postgres import PostgresTable
from src.apps.core.db import connection


QUOTES_TABLE = PostgresTable(connection, 'great_quotes')
QUOTES_SUBSCRIPTIONS_TABLE = PostgresTable(connection, 'quotes_subscriptions')
