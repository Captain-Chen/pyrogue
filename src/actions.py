from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import Engine
    from .entity import Entity

class Action:
    def perform(self, engine: Engine, entity: Entity):
        raise NotImplementedError()

class Escape(Action):
    def perform(self, engine: Engine, entity: Entity):
        raise SystemExit()

class Move(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()
        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity):
        # check the destination tile's position
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.is_in_bounds(dest_x, dest_y):
            return # out of bounds
        
        if not engine.game_map.tiles["is_walkable"][dest_x, dest_y]:
            return # tile cannot be walked on

        entity.move(self.dx, self.dy)
