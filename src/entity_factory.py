from .entity import Actor
from .components.health import Health
from .components.ai import Hostile

player = Actor(
    char="@", 
    color=(255, 255, 255), 
    name="Player",
    ai_cls=Hostile,
    health=Health(30),
    )

rat = Actor(
    char="r",
    color=(128, 128, 128),
    name="Rat",
    ai_cls=Hostile,
    health=Health(8)
)