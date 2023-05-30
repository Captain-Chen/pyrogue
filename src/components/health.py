from .base_component import BaseComponent

class Health(BaseComponent):
    def __init__(self, hp: int):
        self.max_hp = hp
        self._hp = hp

    @property
    def hp(self) -> int:
        return self._hp
    
    @hp.setter
    def hp(self, value: int):
        self._hp = max(0, min(value, self.max_hp))