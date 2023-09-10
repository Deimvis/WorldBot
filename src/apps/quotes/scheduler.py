import calendar, datetime, pytz, time
from src.apps.quotes.api import send_great_quote
from src.apps.quotes.db import QUOTES_SUBSCRIPTIONS_TABLE


class QuotesSubscription:
    class Notification:
        def __init__(self, chat_id, content_type):
            self.chat_id = chat_id
            self.content_type = content_type

    def __init__(self, bot):
        self.bot = bot
        self.notifications = []
        self.update_notifications_list()

    @property
    def time(self):
        timezone = pytz.timezone('Europe/Moscow')
        return datetime.datetime.now(timezone)

    @property
    def next_notification_time(self):
        return (self.time + datetime.timedelta(hours=1)).replace(minute=0, second=0)

    @property
    def next_notification_hour(self):
        return self.next_notification_time.strftime('%H')

    @property
    def next_notification_day_of_week(self):
        return calendar.day_name[self.next_notification_time.weekday()]

    def wait_for_update_notifications_list(self):
        time.sleep((self.next_notification_time - self.time).seconds - 30)

    def wait_for_send_notifications(self, target_hour=None):
        # case when update notifications was too long
        if target_hour and target_hour != self.next_notification_hour:
            return
        time.sleep((self.next_notification_time - self.time).seconds)

    def update_notifications_list(self):
        response_1 = QUOTES_SUBSCRIPTIONS_TABLE.select(where={'type': 'every_day', 'value': self.next_notification_hour})
        response_2 = QUOTES_SUBSCRIPTIONS_TABLE.select(where={'type': 'every_week', 'value': self.next_notification_day_of_week + '-' + self.next_notification_hour})
        self.notifications = []
        for row in (response_1 + response_2):
            notification = self.Notification(row[1], row[2])
            self.notifications.append(notification)

    def send_notifications(self):
        for notification in self.notifications:
            if notification.content_type == 'great_quotes':
                send_great_quote(self.bot, notification.chat_id)

    def run(self):
        while True:
            notification_hour = self.next_notification_hour
            self.wait_for_update_notifications_list()
            self.update_notifications_list()
            self.wait_for_send_notifications(target_hour=notification_hour)
            self.send_notifications()
            time.sleep(10)
