from __future__ import annotations
from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .engine import Engine
    from .entity import Entity

class Action:
    def __init__(self, entity: Entity):
        super().__init__()
        self.entity = entity
    
    @property
    def engine(self) -> Engine:
        return self.entity.gamemap.engine

    def perform(self):
        raise NotImplementedError()
    
class DirectedAction(Action):
    def __init__(self, entity: Entity, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        return self.entity.x + self.dx, self.entity.y + self.dy
    
    @property
    def blocking_entity(self) -> Optional[Entity]:
        return self.engine.game_map.get_entity_at_loc(*self.dest_xy)

    def perform(self, engine: Engine, entity: Entity):
        raise NotImplementedError()

class Escape(Action):
    def perform(self):
        raise SystemExit()

class Move(DirectedAction):
    def perform(self):
        # check the destination tile's position
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.is_in_bounds(dest_x, dest_y):
            return # out of bounds
        
        if not self.engine.game_map.tiles["is_walkable"][dest_x, dest_y]:
            return # tile cannot be walked on
        
        if self.engine.game_map.get_entity_at_loc(dest_x, dest_y):
            return # destination is blocked by an entity

        self.entity.move(self.dx, self.dy)

class Melee(DirectedAction):
    def perform(self):
        target = self.blocking_entity
        if not target:
            return # Nothing at location to attack
        
        print(f"You strike the {target.name} with your fist.")

class Bump(DirectedAction):
    def perform(self):
        if self.blocking_entity:
            return Melee(self.entity, self.dx, self.dy).perform()
        else:
            return Move(self.entity, self.dx, self.dy).perform()