from __future__ import annotations

import copy
from typing import Optional, Tuple, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from .map import Map

T = TypeVar("T", bound="Entity")

class Entity:
    gamemap: Map
    def __init__(
            self, 
            gamemap: Optional[Map] = None,
            x: int = 0, y: int = 0, 
            char: str = "?", color: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            blocks_movement: bool = False,
            ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement

        if gamemap:
            self.gamemap = gamemap
            gamemap.entties.add(self)

    def spawn(self: T, gamemap: Map, x: int, y: int) -> T:
        """Spawn a copy of this instance at given location"""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.gamemap = gamemap
        gamemap.entities.add(clone)

        return clone
    
    def place(self, x: int, y: int, gamemap: Optional[Map] = None):
        self.x = x
        self.y = y

        if gamemap:
            if hasattr(self, "gamemap"):
                self.gamemap.entities.remove(self)
            self.gamemap = gamemap
            gamemap.entities.add(self)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy