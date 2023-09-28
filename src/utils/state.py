from typing import Any


class StateNode:
    def __init__(self):
        self._data = {}
        self._frozen_keys = set()

    def __getitem__(self, key: str) -> Any:
        if key not in self._data:
            self._data[key] = StateNode()
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        assert key not in self._frozen_keys
        self._data[key] = value

    def freeze_key(self, key):
        assert key not in self._frozen_keys
        self._frozen_keys.add(key)
