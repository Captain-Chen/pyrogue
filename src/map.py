import numpy as np
from tcod.console import Console

from . import tile_types

class Map:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        self.visible = np.full((width, height), fill_value=False, order="F") 
        self.explored = np.full((width, height), fill_value=False, order="F") 

    def render(self, console: Console):
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.FOG
        )

    def is_in_bounds(self, x: int, y: int) -> bool:
        return x < self.width and x >= 0 and y < self.height and y >= 0
