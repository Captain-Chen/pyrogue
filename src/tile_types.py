from typing import Tuple
import numpy as np

graphic_dt = np.dtype(
    [
        ("ch", np.int32), # Unicode codepoint
        ("fg", "3B"), # unsigned bytes used for RGB colors
        ("bg", "3B"),
    ]
)

tile_dt = np.dtype(
    [
        ("is_walkable", bool),
        ("is_transparent", bool),
        ("dark", graphic_dt), # When not in FOV
        ("light", graphic_dt), # When in FOV
    ]
)

def new_tile(
        *,
        is_walkable: int,
        is_transparent: int, 
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]]
) -> np.ndarray:
    """
    Helper function for defining individual tile types
    """
    return np.array((is_walkable, is_transparent, dark, light), dtype=tile_dt)

FOG = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
    is_walkable=True, 
    is_transparent=True, 
    dark=(ord(" "), (255, 255, 255), (50, 50, 150)),
    light=(ord(" "), (255, 255, 255), (200, 180, 50))
    )
wall = new_tile(
    is_walkable=False, 
    is_transparent=False, 
    dark=(ord(" "), (255, 255, 255), (0, 0, 100)),
    light=(ord(" "), (255, 255, 255), (130, 110, 50))
    )
