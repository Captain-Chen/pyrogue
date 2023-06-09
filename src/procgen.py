from __future__ import annotations
from typing import Iterator, List, Tuple, TYPE_CHECKING
import random

import tcod

from .map import Map
from . import tile_types
from . import entity_factory

if TYPE_CHECKING:
    from .engine import Engine

class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    def intersects(self, other: RectangularRoom) -> bool:
        return self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y
    
    @property
    def inner(self) -> Tuple[slice, slice]:
        return slice(self.x1 + 1, self.x2), slice(self.y1  + 1, self.y2)
    
def generate_dungeon(
        max_rooms: int,
        min_size: int,
        max_size: int,
        map_width: int,
        map_height: int,
        max_monsters_per_room: int,
        engine: Engine,
        ) -> Map:
    player = engine.player
    dungeon = Map(engine, map_width, map_height, entities=[player])

    rooms: List[RectangularRoom] = []

    # Generate N number of rooms
    for r in range(max_rooms):
        room_width = random.randint(min_size, max_size)
        room_height = random.randint(min_size, max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height -1)

        new_room = RectangularRoom(x, y, room_width, room_height)

        # Check if this room intersects with previously placed rooms. If it does then skip over it.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue

        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            player.place(*new_room.center, dungeon)
        else:
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        spawn_entities(new_room, dungeon, max_monsters_per_room)

        rooms.append(new_room)

    return dungeon

def spawn_entities(room: RectangularRoom, dungeon: Map, max_monsters: int):
    num_monsters = random.randint(0, max_monsters)

    for _ in range(num_monsters):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity_factory.rat.spawn(dungeon, x, y)

def tunnel_between(
        start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Returns an L-shaped tunnel between two points"""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:
        # Move horizontally then vertically
        corner_x, corner_y = x2, y1
    else:
        # Move vertically then horizontally
        corner_x, corner_y = x1, y2

    # Generate coordinates
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y
