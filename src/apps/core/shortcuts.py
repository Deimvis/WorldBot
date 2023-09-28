import telebot
from src.apps.core.types import LanguageCode


def get_language(chat_entity: telebot.types.Message | telebot.types.CallbackQuery) -> LanguageCode:
    # returns ISO639-3 language code
    if isinstance(chat_entity, telebot.types.Message):
        return LanguageCode.from_IETF(chat_entity.from_user.language_code)
    if isinstance(chat_entity, telebot.types.CallbackQuery):
        return LanguageCode.from_IETF(chat_entity.from_user.language_code)
    raise RuntimeError(f'Got unsupported type of chat_entity: {type(chat_entity)}')
