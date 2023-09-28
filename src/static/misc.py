import os
from pathlib import Path
from typing import Dict, List
from src.static.utils import DictBaseModel


class Weekdays(DictBaseModel):
    monday: str
    tuesday: str
    wednesday: str
    thursday: str
    friday: str
    saturday: str
    sunday: str


class Misc(DictBaseModel):
    weekdays: Weekdays


MISC_DATA_FILES: List[Path] = [file for file in (Path(os.getenv('FILES_DIR_PATH')) / 'misc').iterdir()]
MISC_DATA: Dict[str, Misc] = {file.stem.upper(): Misc.model_validate_json(file.read_text()) for file in MISC_DATA_FILES}
