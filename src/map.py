from __future__ import annotations
from typing import Iterable, Optional, TYPE_CHECKING

import numpy as np
from tcod.console import Console

from . import tile_types

if TYPE_CHECKING:
    from .entity import Entity

class Map:
    def __init__(self, width: int, height: int, entities: Iterable[Entity] = ()):
        self.width = width
        self.height = height
        self.entities = set(entities)

        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        self.visible = np.full((width, height), fill_value=False, order="F") 
        self.explored = np.full((width, height), fill_value=False, order="F") 

    def get_entity_at_loc(self, loc_x: int, loc_y: int) -> Optional[Entity]:
        for entity in self.entities:
            if entity.blocks_movement and entity.x == loc_x and entity.y == loc_y:
                return entity
            
            return None

    def render(self, console: Console):
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.FOG
        )

        for entity in self.entities:
            if self.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)


    def is_in_bounds(self, x: int, y: int) -> bool:
        return x < self.width and x >= 0 and y < self.height and y >= 0
