from pydantic import BaseModel
from src.apps.core.types import LanguageCode
from src.utils.state import StateNode


GLOBAL_STATE = StateNode()


class Session(BaseModel):
    interface_language: LanguageCode

    # quotes
    quotes_language: LanguageCode


GLOBAL_STATE['sessions'] = {}
GLOBAL_STATE.freeze_key('sessions')


def clear_state():
    GLOBAL_STATE = StateNode()
    GLOBAL_STATE['sessions'] = {}
    GLOBAL_STATE.freeze_key('sessions')
