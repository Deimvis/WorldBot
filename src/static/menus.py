import os
from pathlib import Path
from pydantic import validator
from typing import Dict, List
from src.static.utils import DictBaseModel


class MainMenu(DictBaseModel):
    quotes_menu: str


class QuotesMenu(DictBaseModel):
    get_quote: str
    subscribe: str
    manage_subscriptions: str


class Subscribing(DictBaseModel):
    class IntervalMenu(DictBaseModel):
        every_day: str
        every_week: str
        return_back: str

    class BaseWeekdayMenu(DictBaseModel):
        monday: str
        tuesday: str
        wednesday: str
        thursday: str
        friday: str
        saturday: str
        sunday: str
        return_back: str

    class TimezoneMenu(DictBaseModel):
        timezone_1: str
        timezone_2: str
        timezone_3: str
        timezone_4: str
        timezone_5: str
        custom_timezone: str
        return_back: str

    class BaseTimeMenu(DictBaseModel):
        base_time_1: str
        base_time_2: str
        base_time_3: str
        base_time_4: str
        base_time_5: str
        custom_base_time: str
        return_back: str

    interval_menu: IntervalMenu
    base_weekday_menu: BaseWeekdayMenu
    timezone_menu: TimezoneMenu
    base_time_menu: BaseTimeMenu


class ManagingSubscriptions(DictBaseModel):
    class MainMenu(DictBaseModel):
        remove: str
        return_back: str


    class RemoveMenu(DictBaseModel):
        button_template: str
        return_back: str

    main_menu: MainMenu
    remove_menu: RemoveMenu


class Menus(DictBaseModel):
    main_menu: MainMenu
    quotes_menu: QuotesMenu
    subscribing: Subscribing
    managing_subscriptions: ManagingSubscriptions


MENUS_DATA_FILES: List[Path] = [file for file in (Path(os.getenv('FILES_DIR_PATH')) / 'menus').iterdir()]
MENUS_DATA: Dict[str, Menus] = {file.stem.upper(): Menus.model_validate_json(file.read_text()) for file in MENUS_DATA_FILES}
