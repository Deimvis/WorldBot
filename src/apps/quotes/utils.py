import requests
import re
from pydantic import BaseModel, validator


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


class Quote(BaseModel):
    author: str
    text: str

    @validator('author')
    def is_author_valid(cls, v):
        assert 0 <= len(v) <= 1000, 'Author name is too long'
        return v


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
