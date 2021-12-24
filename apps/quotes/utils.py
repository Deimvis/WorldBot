import os
import requests
import re
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

class Quote:
    def __init__(self, text=None, author=None):
        self.text = text
        self.author = author

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

def get_great_quotes_list():
    r = requests.get('https://www.forbes.ru/forbeslife/dosug/262327-na-vse-vremena-100-vdokhnovlyayushchikh-tsitat')
    parsed_ = re.findall(r'class="article-node-text">.*?</div', r.text)

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
    db = QuotesSQLiteDatabase(os.getenv('DB_PATH', 'db.db'))
    great_quotes = get_great_quotes_list()
    for quote in great_quotes:
        db.add_great_quote(quote)
