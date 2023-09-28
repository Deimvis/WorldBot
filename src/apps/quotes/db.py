import random
from lib.storages.postgres import PostgresTable
from src.apps.core.db import connection
from src.apps.core.types import LanguageCode
from src.apps.quotes.types import Quote


QUOTE_TABLE = PostgresTable(connection, 'quote')
QUOTES_SUBSCRIPTION_TABLE = PostgresTable(connection, 'quotes_subscription')


def get_random_quote(language: LanguageCode) -> Quote | None:
    great_quotes = QUOTE_TABLE.select(where={'language': language.name})
    if len(great_quotes) == 0:
        return None
    quote = random.choice(great_quotes)
    return Quote.from_database_row(quote)
