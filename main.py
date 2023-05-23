import tcod
import os

from src.engine import Engine
from src.procgen import generate_dungeon
from src.input_handlers import EventHandler
from src.entity import Entity

res_folder = os.path.join(os.path.dirname(__file__), "res")

def main():
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 40

    my_tileset = tcod.tileset.load_tilesheet(
        os.path.join(res_folder, "dejavu10x10_gs_tc.png"), 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = Entity(int(screen_width / 2), int(screen_height / 2), '@', (255, 255, 255))
    npc = Entity(int(screen_width / 2) - 5, int(screen_height / 2), "S", (255, 255, 0))
    entities = {player, npc}
    game_map = generate_dungeon(
        max_rooms=30,
        min_size=6,
        max_size=10,
        map_width=map_width,
        map_height=map_height,
        player=player
        )

    engine = Engine(entities, EventHandler(), game_map, player)

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=my_tileset,
        title="Ye Honk Dungeon",
        vsync=True,
    ) as context:
        rc = tcod.Console(screen_width, screen_height, order='F')

        # main game loop
        while True:
            engine.render(rc, context)
            events = tcod.event.wait()
            engine.handle_events(events)
                
if __name__ == "__main__":
    main()