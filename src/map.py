from __future__ import annotations
from typing import Iterable, Iterator, Optional, TYPE_CHECKING

import numpy as np
from tcod.console import Console

from . import tile_types
from .entity import Actor

if TYPE_CHECKING:
    from .engine import Engine
    from .entity import Entity

class Map:
    def __init__(self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()):
        self.engine = engine
        self.width = width
        self.height = height
        self.entities = set(entities)

        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        self.visible = np.full((width, height), fill_value=False, order="F") 
        self.explored = np.full((width, height), fill_value=False, order="F") 

    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over this map's living Actors"""
        yield from (
            entity for entity in self.entities if isinstance(entity, Actor) and entity.is_alive
        )
    
    def get_entity_at_loc(self, loc_x: int, loc_y: int) -> Optional[Entity]:
        for entity in self.entities:
            if entity.blocks_movement and entity.x == loc_x and entity.y == loc_y:
                return entity
        return None
    
    def get_actor_at_loc(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
        return None

    def render(self, console: Console):
        console.tiles_rgb[0: self.width, 0: self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.FOG
        )

        for entity in self.entities:
            if self.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)


    def is_in_bounds(self, x: int, y: int) -> bool:
        return x < self.width and x >= 0 and y < self.height and y >= 0
