from pydantic import BaseModel, validator
from src.utils.state import StateNode


GLOBAL_STATE = StateNode()


class Session(BaseModel):
    interface_language: str

    # quotes
    quotes_language: str

    @validator('interface_language')
    def is_interface_language_valid(cls, v):
        cls.assert_satisfy_ISO639_3(v)
        return v

    @validator('quotes_language')
    def is_quotes_language_valid(cls, v):
        cls.assert_satisfy_ISO639_3(v)
        return v

    @classmethod
    def assert_satisfy_ISO639_3(cls, v):
        assert v in ('RUS', 'ENG')


GLOBAL_STATE['sessions'] = {}
GLOBAL_STATE.reserve_key('sessions')
