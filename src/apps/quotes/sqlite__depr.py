import sqlite3


QuotesSubscriptionsLIMIT = 5


class QuotesSubscriptionsLimitException(Exception):
    def __init__(self, message='Не получилось оформить подписку:\n'
                               'Превышено допустимое количество подписок на выбранные цитаты для данного чата'):
        self.message = message

    def __str__(self):
        return self.message


class QuotesSQLiteDatabase:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def execute(self, query, *args):
        with self.connection:
            return self.cursor.execute(query, [arg for arg in args]).fetchall()

    def get_great_quotes(self):
        query = 'SELECT * FROM great_quotes'
        return self.execute(query)

    def add_great_quote(self, quote):
        query = 'INSERT INTO great_quotes (text, author) VALUES (?,?)'
        self.execute(query, quote.text, quote.author)

    def get_quotes_subscriptions(self, type=None, value=None):
        query = 'SELECT * FROM quotes_subscriptions '
        if type is not None and value is not None:
            query += 'WHERE type=? and value=?'
            return self.execute(query, type, value)
        if type is not None:
            query += 'WHERE type=?'
            return self.execute(query, type)
        if value is not None:
            query += 'WHERE value=?'
            return self.execute(query, value)
        return self.execute(query)

    def count_chat_subscriptions(self, chat_id, name):
        query = 'SELECT COUNT(*) FROM quotes_subscriptions WHERE chat_id=? and name=?'
        return self.execute(query, chat_id, name)[0][0]

    def add_quotes_subscriber(self, chat_id, name, type, value):
        if self.count_chat_subscriptions(chat_id, name) >= QuotesSubscriptionsLIMIT:
            raise QuotesSubscriptionsLimitException
        query = 'INSERT INTO quotes_subscriptions (chat_id, name, type, value) VALUES (?,?,?,?)'
        return self.execute(query, chat_id, name, type, value)

    def get_quotes_subscriptions_for_chat(self, chat_id):
        query = 'SELECT * FROM quotes_subscriptions WHERE chat_id=?'
        return self.execute(query, chat_id)

    def remove_quotes_subscriber(self, chat_id, name, type, value):
        query = 'DELETE FROM quotes_subscriptions WHERE chat_id=? and name=? and type=? and value=?'
        return self.execute(query, chat_id, name, type, value)

    def remove_quotes_subscription(self, id):
        query = 'DELETE FROM quotes_subscriptions WHERE id=?'
        return self.execute(query, id)

    def has_user(self, chat_id):
        query = 'SELECT EXISTS(SELECT 1 FROM users WHERE chat_id=?)'
        return self.execute(query, chat_id)

    def add_user(self, chat_id, username, first_name, last_name):
        query = 'INSERT INTO users (chat_id, username, first_name, last_name) VALUES (?,?,?,?)'
        return self.execute(query, chat_id, username, first_name, last_name)

    def remove_user(self, chat_id, username, first_name, last_name):
        query = 'DELETE FROM users WHERE chat_id=? and username=? and first_name=? and last_name=?'
        return self.execute(query, chat_id, username, first_name, last_name)

    def update_user(self, chat_id, username, first_name, last_name):
        query = 'REPLACE INTO users (chat_id, username, first_name, last_name) VALUES (?,?,?,?)'
        return self.execute(query, chat_id, username, first_name, last_name)

    def close(self):
        self.connection.close()
