import telebot
import time
from collections import deque
from src.apps.core.state import GLOBAL_STATE
from src.apps.core.types import LanguageCode


def get_language(chat_entity: telebot.types.Message | telebot.types.CallbackQuery) -> LanguageCode:
    """ Returns ISO639-3 language code """
    if isinstance(chat_entity, telebot.types.Message):
        return LanguageCode.from_IETF(chat_entity.from_user.language_code)
    if isinstance(chat_entity, telebot.types.CallbackQuery):
        return LanguageCode.from_IETF(chat_entity.from_user.language_code)
    raise RuntimeError(f'Got unsupported type of chat_entity: {type(chat_entity)}')


def flood_trigger(chat_id: int) -> bool:
    now = int(time.time())
    GLOBAL_STATE['bad_message'][chat_id]['queue'] = GLOBAL_STATE['bad_message'][chat_id].get('queue', deque())
    queue = GLOBAL_STATE['bad_message'][chat_id]['queue']
    while queue and now - queue[0] >= 10:
        queue.popleft()
    queue.append(now)
    is_flooding = len(queue) >= 10
    if is_flooding:
        queue.clear()
    return is_flooding
