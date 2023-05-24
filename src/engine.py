from typing import Iterable, Any
from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from .entity import Entity
from .input_handlers import EventHandler
from .map import Map

class Engine:
    def __init__(self, event_handler: EventHandler, game_map: Map, player: Entity):
        self.event_handler = event_handler
        self.player = player
        self.game_map = game_map
        self.update_fov() # call method at initialization so FoV is created at start

    def handle_enemy_turns(self):
        for entity in self.game_map.entities - {self.player}:
            pass

    def handle_events(self, events: Iterable[Any]):
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            action.perform(self, self.player)
            self.update_fov() # Update the FOV before the next action

    def update_fov(self):
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["is_transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        self.game_map.explored |= self.game_map.visible
            
    def render(self, console: Console, context: Context):
        self.game_map.render(console)
        context.present(console)
        console.clear()