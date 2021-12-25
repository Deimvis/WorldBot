import requests
import re
from config import DB_PATH
from apps.quotes.sqlite import QuotesSQLiteDatabase


DayOfWeekRUEN = {
    'понедельник' : 'Monday',
    'вторник' : 'Tuesday',
    'среда' : 'Wednesday',
    'четверг' : 'Thursday',
    'пятница' : 'Friday',
    'суббота' : 'Saturday',
    'воскресенье' : 'Sunday'
}

DayOfWeekENRU = {
    'monday' : 'Понедельник',
    'tuesday' : 'Вторник',
    'wednesday' : 'Среда',
    'thursday' : 'Четверг',
    'friday' : 'Пятница',
    'saturday' : 'Суббота',
    'sunday' : 'Воскресенье'
}


class Quote:
    def __init__(self, text=None, author=None):
        self.text = text
        self.author = author


class Subscription:
    def __init__(self, db_row):
        self.id = db_row[0]
        self.chat_id = db_row[1]
        self.name = db_row[2]
        self.type = db_row[3]
        self.value = db_row[4]

    def beautify(self):
        result = dict()
        result['id'] = self.id
        if self.name == 'great_quotes':
            result['name'] = '🔥 Великая цитата'
        else:
            result['name'] = 'UNKNOWN'
        if self.type == 'every_day':
            result['type'] = 'Каждый день в {}:00'.format(self.value)
        elif self.type == 'every_week':
            result['type'] = 'Каждую неделю'
            day_of_week, time = self.value.split('-')
            day_of_week_ru = DayOfWeekENRU[day_of_week.lower()]
            result['type'] += ' в {}, {}:00'.format(day_of_week_ru, time)
        else:
            result['type'] = 'UNKNOWN'
        return result

    @staticmethod
    def beautify_db_row(row):
        result = dict()
        result['id'] = row[0]
        if row[1] == 'great_quotes':
            result['name'] = '🔥 Великая цитата'
        else:
            result['name'] = 'UNKNOWN'
        if row[2] == 'every_day':
            result['type'] = 'Каждый день в {}:00'.format(row[3])
        elif row[2] == 'every_week':
            result['type'] = 'Каждую неделю в {}:00'.format(row[3])
        else:
            result['type'] = 'UNKNOWN'
        return result


def get_build_quotes_subscription_status(chat_id, build_quotes_subscription):
    cond1 = chat_id in build_quotes_subscription
    if not cond1:
        return 'EMPTY'
    cond2 = build_quotes_subscription[chat_id].get('name', None) is not None
    cond3 = build_quotes_subscription[chat_id].get('type', None) is not None
    if cond2 and cond3:
        return 'need value'
    elif cond2:
        return 'need type'
    else:
        return 'need name'


def get_remove_quotes_subscription_status(chat_id, remove_quotes_subscription_stage):
    if chat_id not in remove_quotes_subscription_stage:
        return 'EMPTY'
    return 'need select'


def get_great_quotes_list():
    r = requests.get('https://www.forbes.ru/forbeslife/dosug/262327-na-vse-vremena-100-vdokhnovlyayushchikh-tsitat')
    parsed_ = re.findall(r'<p class="yl27R" style="text-align:left;">.*?</p>', r.text)

    quote_text = []
    authors = []
    for i in range(len(parsed_)):
        string = parsed_[i]
        if (i % 2 == 0):
            text = re.search(r'[а-яА-Я].*?<', string)
            quote_text.append(text[0] if text else None)
        else:
            author = re.search(r'[а-яА-Я].*?<', string)
            authors.append(author[0] if author else None)

    quote_text = list(map(lambda string: string[:len(string) - 1].strip(), quote_text))
    authors = list(map(lambda string: string[:len(string) - 1].strip(), authors))

    quotes = []
    for text, author in zip(quote_text, authors):
        quote = Quote(text, author)
        quotes.append(quote)

    return quotes


def update_great_quotes():
    db = QuotesSQLiteDatabase(DB_PATH)
    great_quotes = get_great_quotes_list()
    for quote in great_quotes:
        db.add_great_quote(quote)
