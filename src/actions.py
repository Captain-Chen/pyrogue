from __future__ import annotations
from typing import Optional, Tuple, TYPE_CHECKING
import random

if TYPE_CHECKING:
    from .engine import Engine
    from .entity import Entity, Actor

class Action:
    def __init__(self, entity: Actor):
        super().__init__()
        self.entity = entity
    
    @property
    def engine(self) -> Engine:
        return self.entity.game_map.engine

    def perform(self):
        raise NotImplementedError()
    
class DirectedAction(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Return destination coordinates"""
        return self.entity.x + self.dx, self.entity.y + self.dy
    
    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return blocking entity at this location"""
        return self.engine.game_map.get_entity_at_loc(*self.dest_xy)
    
    @property
    def target_actor(self) -> Optional[Actor]:
        """Return actor at this destination"""
        return self.engine.game_map.get_actor_at_loc(*self.dest_xy)

    def perform(self, engine: Engine, entity: Entity):
        raise NotImplementedError()

class Escape(Action):
    def perform(self):
        raise SystemExit()
    
class Wait(Action):
    def perform(self):
        pass

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
        target = self.target_actor
        if not target:
            return # Nothing at location to attack
        
        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}!"
        attack_dmg = random.randint(3, 10)

        print(f"{attack_desc} {target.name} takes {attack_dmg} points of damage.")
        target.health.hp -= attack_dmg

        if target.health.hp <= 0:
            print(f"{target.name} was defeated.")
            target.ai = None
            target.blocks_movement = False
            target.char = "%"
            target.color = (191, 0, 0)
            target.name = f"remains of {target.name}"

class Bump(DirectedAction):
    def perform(self):
        if self.blocking_entity:
            return Melee(self.entity, self.dx, self.dy).perform()
        else:
            return Move(self.entity, self.dx, self.dy).perform()