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
        ("dark", graphic_dt),
    ]
)

def new_tile(
        *,
        is_walkable: int,
        is_transparent: int, 
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """
    Helper function for definining individual tile types
    """
    return np.array((is_walkable, is_transparent, dark), dtype=tile_dt)

floor = new_tile(is_walkable=True, is_transparent=True, dark=(ord(" "), (255, 255, 255), (50, 50, 150)))
wall = new_tile(is_walkable=False, is_transparent=False, dark=(ord(" "), (255, 255, 255), (0, 0, 100)))