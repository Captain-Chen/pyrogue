from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING

import numpy as np # type: ignore
import tcod

from ..actions import Action, Melee, Move, Wait
from .base_component import BaseComponent

if TYPE_CHECKING:
    from ..entity import Actor

class BaseAI(Action, BaseComponent):
    entity: Actor

    def perform(self):
        raise NotImplementedError()
    
    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        """
        Computes and return a path to the target position.
        If there is no valid path it returns an empty list.
        """

        # Make a copy of the is_walkable array
        cost = np.array(self.entity.game_map.tiles["is_walkable"], dtype=np.int8)

        for entity in self.entity.game_map.entities:
            # Check if entity blocks movement and cost is not zero (blocking)
            if entity.blocks_movement and cost[entity.x, entity.y]:
                """
                Add to the cost of a blocked position
                Lower number means more enemies will crowd around each other in hallways
                Higher number means enemies will take longer paths in order to surround the player
                """
                cost[entity.x, entity.y] += 10

        # Create a graph from the cost array and pass it to a new pathfinder
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        # Start position
        pathfinder.add_root((self.entity.x, self.entity.y))

        # Compute path to destination and remove the starting point
        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # Convert from a List[List[int]] to List[Tuple[int, int]]
        return [(index[0], index[1]) for index in path]
    
class Hostile(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self):
        target = self.engine.player
        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy)) # Chebyshev distance

        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                return Melee(self.entity, dx, dy).perform()
            
            self.path = self.get_path_to(target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop()
            return Move(
                self.entity, dest_x - self.entity.x, dest_y - self.entity.y
            ).perform()
        
        return Wait(self.entity).perform()
            
