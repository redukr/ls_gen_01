
from dataclasses import dataclass
from typing import Optional

@dataclass
class CardStats:
    atk: int = 0
    def: int = 0
    stb: int = 0
    init: int = 0
    rng: int = 0
    move: int = 0

@dataclass
class Card:
    name: str
    type: str
    cost: int
    cost_type: str
    stats: Optional[CardStats] = None
    description: str = ""
    image_path: Optional[str] = None

    def __post_init__(self):
        if self.stats is None and self.type == "unit":
            self.stats = CardStats()

    def is_unit(self) -> bool:
        return self.type == "unit"

    def is_tactic(self) -> bool:
        return self.type == "tactic"

    def is_equipment(self) -> bool:
        return self.type == "equipment"

    def is_event(self) -> bool:
        return self.type == "event"

    def is_thematic(self) -> bool:
        return self.type == "thematic"
