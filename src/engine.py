from __future__ import annotations

from typing import TYPE_CHECKING

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from .input_handlers import EventHandler

if TYPE_CHECKING:
    from .entity import Actor
    from .map import Map

class Engine:
    game_map: Map

    def __init__(self, player: Actor):
        self.event_handler: EventHandler = EventHandler(self)
        self.player = player

    def handle_enemy_turns(self):
        for entity in self.game_map.entities - {self.player}:
            if entity.ai:
                entity.ai.perform()

    def update_fov(self):
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["is_transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        self.game_map.explored |= self.game_map.visible
            
    def render(self, console: Console, context: Context):
        self.game_map.render(console)
        console.print(1, 47, string=f"Hit Points: {self.player.health.hp}/{self.player.health.max_hp}")
        context.present(console)
        console.clear()