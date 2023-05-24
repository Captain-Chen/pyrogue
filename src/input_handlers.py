from typing import Optional, TYPE_CHECKING
import tcod.event
from .actions import Action, Escape, Bump

class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()
    
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None
        key = event.sym
        match key:
            case tcod.event.K_UP:
                action = Bump(0, -1)
            case tcod.event.K_DOWN:
                action = Bump(0, 1)
            case tcod.event.K_LEFT:
                action = Bump(-1, 0)
            case tcod.event.K_RIGHT:
                action = Bump(1, 0)
            case tcod.event.K_ESCAPE:
                action = Escape()
            
        return action