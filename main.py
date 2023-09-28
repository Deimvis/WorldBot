import os
import logging
import threading
import traceback
import telebot
import src.apps.core as core
import src.apps.quotes as quotes
from src.apps.quotes.notifier import QuoteNotifier


if os.getenv('DEBUG'):
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
        datefmt="%d/%b/%Y %H:%M:%S",
    )
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('yt').setLevel(logging.WARNING)
else:
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
        datefmt="%d/%b/%Y %H:%M:%S",
    )


def main():
    bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
    quotes.register_handlers(bot)
    core.register_handlers(bot)

    notifier = QuoteNotifier(bot)
    notifier_thread = threading.Thread(target=notifier.run)
    notifier_thread.start()

    while True:
        try:
            bot.polling(non_stop=True)
        except Exception as error:
            error_msg = f'---ERROR---\nError:{error}\nTraceback:{traceback.format_exc()}'
            logging.error(error_msg)
            if os.getenv('DEBUG_CHAT_ID'):
                lines = error_msg.split('\n')
                for line_ind in range(0, len(lines), 20):
                    bot.send_message(os.getenv('DEBUG_CHAT_ID'), '\n'.join(lines[line_ind:line_ind+20]))


if __name__ == '__main__':
    main()
