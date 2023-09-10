import random
from telebot import types
from src.apps.quotes.utils import Subscription
from src.apps.quotes.db import QUOTES_TABLE, QUOTES_SUBSCRIPTIONS_TABLE

QuotesSubscriptionsLIMIT = 5


class QuotesSubscriptionsLimitException(Exception):
    def __init__(self, message='Не получилось оформить подписку:\n'
                               'Превышено допустимое количество подписок на выбранные цитаты для данного чата'):
        self.message = message

    def __str__(self):
        return self.message

def quotes_menu():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_great_quote = types.KeyboardButton('🔥 Великая цитата')
    button_quote_subscription = types.KeyboardButton('✉️ Хочу регулярно получать цитаты')
    button_quote_subscription_manage = types.KeyboardButton('⚙️ Управление подписками')
    markup.add(button_great_quote)
    markup.add(button_quote_subscription)
    markup.add(button_quote_subscription_manage)
    return markup


def quotes_subscription_name_menu():
    markup = types.InlineKeyboardMarkup()
    button_great_quote_subscription = types.InlineKeyboardButton('🔥 Великая цитата', callback_data='great_quotes')
    button_return = types.InlineKeyboardButton('Вернуться назад', callback_data='quotes_menu')
    markup.add(button_great_quote_subscription)
    markup.add(button_return)
    return markup


def quotes_subscription_type_menu():
    markup = types.InlineKeyboardMarkup()
    button_every_day = types.InlineKeyboardButton('Каждый день', callback_data='every_day')
    button_every_week = types.InlineKeyboardButton('Каждую неделю', callback_data='every_week')
    markup.add(button_every_day)
    markup.add(button_every_week)
    return markup


def quotes_subscription_everyday_value_menu():
    markup = types.InlineKeyboardMarkup()
    button_10 = types.InlineKeyboardButton('10:00', callback_data='10')
    button_11 = types.InlineKeyboardButton('11:00', callback_data='11')
    button_12 = types.InlineKeyboardButton('12:00', callback_data='12')
    button_13 = types.InlineKeyboardButton('13:00', callback_data='13')
    button_14 = types.InlineKeyboardButton('14:00', callback_data='14')
    button_15 = types.InlineKeyboardButton('15:00', callback_data='15')
    button_other = types.InlineKeyboardButton('Укажу своё', callback_data='other')
    markup.add(button_10)
    markup.add(button_11)
    markup.add(button_12)
    markup.add(button_13)
    markup.add(button_14)
    markup.add(button_15)
    markup.add(button_other)
    return markup


def quotes_subscription_manage_menu():
    markup = types.InlineKeyboardMarkup()
    button_remove_subscription = types.InlineKeyboardButton('Удалить подписку',
                                                            callback_data='remove_quotes_subscription')
    button_return = types.InlineKeyboardButton('Вернуться назад', callback_data='quotes_menu')
    markup.add(button_remove_subscription)
    markup.add(button_return)
    return markup


def remove_quotes_subscriptions_menu(subscriptions_cnt):
    subscriptions_cnt = min(subscriptions_cnt, 5)
    markup = types.InlineKeyboardMarkup()
    for i in range(1, subscriptions_cnt + 1):
        button = types.InlineKeyboardButton(str(i), callback_data='remove_subscription_{}'.format(i))
        markup.add(button)
    button_return = types.InlineKeyboardButton('Вернуться назад', callback_data='quotes_menu')
    markup.add(button_return)
    return markup


def send_quotes_menu(bot, chat_id):
    way = random.randint(1, 7)
    message = None
    if way == 1:
        heads = ['🐶', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🦁', '🐵', '🙈']
        message = 'Выбирай, что по душе {}'.format(random.choice(heads))
    elif way == 2:
        message = 'Цитаты? А новогодние будут? С подааарками ☃️'
    elif way == 3:
        message = 'До Нового Года совсем чуть-чуть, а ты еще не все мудрости познал!\nДавай исправлять!🍀'
    elif way == 4:
        message = '🧸\nЯ просто оставлю его здесь.\nТак... чтобы тебе нескучно было🙂️'
    elif way == 5:
        message = 'А ты тоже умеешь её рисовать?\n 🦉 = ⭕ + ⭕ + ✨'
    elif way == 6:
        message = '"Несмотря ни на какие препятствия, я буду идти к своей цели"'
    elif way == 7:
        message = 'Говорят, чудеса на Новый Год и вправду случаются!\nОсобенно если их творишь именно ты ✨'
    return bot.send_message(chat_id, message, reply_markup=quotes_menu())


def send_quotes_subscription_menu(bot, chat_id):
    message_text = 'Супер!\nВыбирай раздел цитат, на который хотел бы подписаться!'
    bot.send_message(chat_id, message_text, reply_markup=quotes_subscription_name_menu())


def send_quotes_subscription_manage_menu(bot, chat_id):
    bot.send_message(chat_id, 'Надеюсь, всё в порядке?', reply_markup=quotes_subscription_manage_menu())


def send_great_quote(bot, chat_id):
    great_quotes = QUOTES_TABLE.select()
    quote = random.choice(great_quotes)
    response = '{text}\n_{author}_'.format(text=quote[1], author=quote[2])
    bot.send_message(chat_id, response, parse_mode='Markdown', reply_markup=quotes_menu())


def handle_quotes_subscription(bot, chat_id, subscription):
    try:
        if QUOTES_SUBSCRIPTIONS_TABLE.count(where={'chat_id': chat_id, 'name': subscription['name']}) >= QuotesSubscriptionsLIMIT:
            raise QuotesSubscriptionsLimitException
        QUOTES_SUBSCRIPTIONS_TABLE.insert([{'chat_id': chat_id} | subscription])
        QUOTES_SUBSCRIPTIONS_TABLE.commit()
    except QuotesSubscriptionsLimitException as e:
        return bot.send_message(chat_id, str(e), reply_markup=quotes_menu())
    bot.send_message(chat_id, '🎉 Поздравляю! Подписка оформлена!', reply_markup=quotes_menu())


def handle_remove_quote_subscription(bot, chat_id, message_id, remove_quotes_subscription_stage):
    subscriptions = QUOTES_SUBSCRIPTIONS_TABLE.select(where={'chat_id': chat_id})
    subscriptions.sort(key=lambda row: row[0])
    if len(subscriptions) == 0:
        bot.send_message(chat_id, 'У Вас нет активных подписок на цитаты', reply_markup=quotes_menu())
    subscriptions = subscriptions[:min(len(subscriptions), 5)]
    subscriptions = [Subscription(row) for row in subscriptions]
    message = 'Выбери подписку для удаления:\n'
    remove_quotes_subscription_stage[chat_id] = []
    for ind, sub in enumerate(subscriptions):
        s = sub.beautify()
        message += '**{}** | {} | {}\n'.format(ind + 1, s['name'], s['type'])
        remove_quotes_subscription_stage[chat_id].append(sub)
    menu = remove_quotes_subscriptions_menu(len(subscriptions))
    return bot.edit_message_text(message, chat_id, message_id, parse_mode='Markdown', reply_markup=menu)


def handle_remove_quote_subscription_do(bot, chat_id, selected_subscription):
    QUOTES_SUBSCRIPTIONS_TABLE.delete(where={'id': selected_subscription.id})
    QUOTES_SUBSCRIPTIONS_TABLE.commit()
    end_with = random.choice(['💣', '🔫', '⚰', '️🪦', '🔨'])
    return bot.send_message(chat_id, 'Подписка успешно удалена {}'.format(end_with), reply_markup=quotes_menu())
