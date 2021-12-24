import calendar, datetime, pytz, time
from config import DB_PATH
from apps.quotes.api import send_great_quote
from apps.quotes.sqlite import QuotesSQLiteDatabase


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

    def update_notifications_list(self):
        db = QuotesSQLiteDatabase(DB_PATH)
        response_1 = db.get_quotes_subscriptions('every_day', self.next_notification_hour)
        response_2 = db.get_quotes_subscriptions('every_week',
                                                 self.next_notification_day_of_week + '-' + self.next_notification_hour)
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
            time.sleep((self.next_notification_time - self.time).seconds)
            self.send_notifications()
            self.update_notifications_list()
