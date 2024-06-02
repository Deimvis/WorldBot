import datetime
import logging
import pytz
import time
import traceback
import src.apps.quotes.api as api
from src.apps.quotes.db import QUOTES_SUBSCRIPTION_TABLE
from src.apps.quotes.types import Subscription


class QuoteNotifier:
    def __init__(self, bot):
        self.bot = bot

    def run(self):
        while True:
            try:
                self.notify_everyone()
            except Exception as error:
                error_msg = f'Error: {error}\nTraceback:\n{traceback.format_exc()}'
                logging.error(f'Something went wrong!\n{error_msg}')
            time.sleep(60 - datetime.datetime.now().second)

    def notify_everyone(self):
        for row in QUOTES_SUBSCRIPTION_TABLE.select():
            subscription = Subscription.from_database_row(row)
            if self.is_right_time(subscription):
                self.send(subscription)

    def is_right_time(self, subscription: Subscription) -> bool:
        now = datetime.datetime.now(tz=pytz.timezone(subscription.timezone))
        if subscription.base_minute != now.minute:
            return False
        if subscription.base_hour != now.hour:
            return False
        if subscription.base_weekday is not None and subscription.base_weekday != now.weekday():
            return False
        return True

    def send(self, subscription: Subscription) -> None:
        logging.debug(f'Sending quote to "{subscription.chat_id}"... ({datetime.datetime.now()})')
        try:
            api.send_quote(self.bot, subscription.chat_id, subscription.language)
        except Exception as error:
            status_msg = f'Failed to send quote to "{subscription.chat_id}" ({datetime.datetime.now()})'
            error_msg = f'Error: {error}\nTraceback:\n{traceback.format_exc()}'
            logging.error(f'{status_msg}\n{error_msg}')
