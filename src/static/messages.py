import os
import random
from pathlib import Path
from pydantic import ConfigDict, ValidationInfo, field_validator
from typing import Dict, List, Tuple, Union
from src.static.utils import DictBaseModel


class Shortcuts:
    def r(self) -> str:
        return self.resolve()


class PlainMessage(str, Shortcuts):
    def resolve(self) -> str:
        return str(self)


class RandomMessage(list, Shortcuts):
    def resolve(self) -> str:
        return random.choice(self)


class ProbabilisticMessage(DictBaseModel, Shortcuts):
    type: str
    options: List[Tuple[float, str]]

    @field_validator('type')
    @classmethod
    def type_is_valid(cls, v):
        assert v == 'probabilistic'
        return v

    @field_validator('options')
    @classmethod
    def values_is_valid(cls, v):
        total_probability = 0
        for probability, _ in v:
            assert 0 <= probability <= 1, 'Probability is out of range [0, 1]'
            total_probability += probability
        assert total_probability == 1.0, 'Total probability is not 1.0'
        return v

    def resolve(self) -> str:
        return random.choices(self.options.values(), weights=[float(prob) for prob in self.options.keys()])


Message = str | List[str] | ProbabilisticMessage

class MessageDict(DictBaseModel):
    @field_validator('*')
    @classmethod
    def random_messages_are_valid(cls, v, info: ValidationInfo):
        if isinstance(v, str):
            if v.startswith('@FILE:'):
                file = Path(os.getenv('FILES_DIR_PATH')) / 'messages' / v.lstrip('@FILE:')
                return PlainMessage(file.read_text())
            return PlainMessage(v)
        if isinstance(v, list):
            assert len(v) >= 1, 'Empty options list for random message'
            return RandomMessage(v)
        return v


class Quoting(MessageDict):
    no_quotes: Message
    quote_template: Message


class Subscribing(MessageDict):
    max_subscriptions_reached: Message
    interval_step: Message
    base_weekday_step: Message
    timezone_step: Message
    custom_timezone_step: Message
    bad_custom_timezone: Message
    base_time_step: Message
    custom_base_time_step: Message
    bad_custom_base_time: Message
    congratulations: Message
    done_template: Message
    cancelled: Message
    unexpected_error: Message


class ManagingSubscriptions(MessageDict):
    no_subscriptions: Message
    subscription_not_found: Message
    subscription_line_template: Message
    main_menu_template: Message
    remove_menu_template: Message
    removing_done_template: Message


class Messages(MessageDict):
    start: Message
    bad_message_reaction: Message
    quotes_menu: Message
    quoting: Quoting
    subscribing: Subscribing
    managing_subscriptions: ManagingSubscriptions
    last_updates: Message
    about: Message


MESSAGES_DATA_FILES: List[Path] = [file for file in (Path(os.getenv('FILES_DIR_PATH')) / 'messages').iterdir() if file.is_file()]
MESSAGES_DATA: Dict[str, Messages] = {file.stem.upper(): Messages.model_validate_json(file.read_text()) for file in MESSAGES_DATA_FILES}
