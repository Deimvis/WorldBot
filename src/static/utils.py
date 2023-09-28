from pydantic import BaseModel


class DictBaseModel(BaseModel):
    def __getitem__(self, key):
        return getattr(self, key)
