from __future__ import annotations

import copy
from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from .map import Map
    from components.ai import BaseAI
    from components.health import Health

T = TypeVar("T", bound="Entity")

class Entity:
    game_map: Map
    def __init__(
            self, 
            game_map: Optional[Map] = None,
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

        if game_map:
            self.game_map = game_map
            game_map.entities.add(self)

    def spawn(self: T, game_map: Map, x: int, y: int) -> T:
        """Spawn a copy of this instance at given location"""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.game_map = game_map
        game_map.entities.add(clone)

        return clone
    
    def place(self, x: int, y: int, game_map: Optional[Map] = None):
        self.x = x
        self.y = y

        if game_map:
            if hasattr(self, "game_map"):
                self.game_map.entities.remove(self)
            self.game_map = game_map
            game_map.entities.add(self)

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

class Actor(Entity):
    def __init__(
            self,
            *,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            color: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            ai_cls: Type[BaseAI],
            health: Health
    ):
        super().__init__(
            x=x, 
            y=y, 
            char=char, 
            color=color,
            name=name,
            blocks_movement=True
            )
        
        self.ai: Optional[BaseAI] = ai_cls(self)
        self.health = health
        self.health.entity = self

    @property
    def is_alive(self) -> bool:
        return bool(self.ai)