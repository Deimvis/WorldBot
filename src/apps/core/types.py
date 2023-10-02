from enum import Enum


class LanguageCode_ISO639_3(Enum):
    ENG = 1
    RUS = 2

    @staticmethod
    def from_IETF(IETF_language_code: str):
        if IETF_language_code == 'ru':
            return LanguageCode_ISO639_3.RUS
        return LanguageCode_ISO639_3.ENG


LanguageCode = LanguageCode_ISO639_3
