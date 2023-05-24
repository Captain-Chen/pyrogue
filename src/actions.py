from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import Engine
    from .entity import Entity

class Action:
    def perform(self, engine: Engine, entity: Entity):
        raise NotImplementedError()
    
class DirectedAction:
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity):
        raise NotImplementedError()

class Escape(Action):
    def perform(self, engine: Engine, entity: Entity):
        raise SystemExit()

class Move(DirectedAction):
    def perform(self, engine: Engine, entity: Entity):
        # check the destination tile's position
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.is_in_bounds(dest_x, dest_y):
            return # out of bounds
        
        if not engine.game_map.tiles["is_walkable"][dest_x, dest_y]:
            return # tile cannot be walked on
        
        if engine.game_map.get_entity_at_loc(dest_x, dest_y):
            return # destination is blocked by an entity

        entity.move(self.dx, self.dy)

class Melee(DirectedAction):
    def perform(self, engine: Engine, entity: Entity):
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        target = engine.game_map.get_entity_at_loc(dest_x, dest_y)
        if not target:
            return # Nothing at location to attack
        
        print(f"You strike the {target.name} with your fist.")

class Bump(DirectedAction):
    def perform(self, engine: Engine, entity):
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if engine.game_map.get_entity_at_loc(dest_x, dest_y):
            return Melee(self.dx, self.dy).perform(engine, entity)
        else:
            return Move(self.dx, self.dy).perform(engine, entity)