from dataclasses import dataclass
from typing import Tuple, Optional

@dataclass
class DurableItem:
    """Represents an item that has durability."""
    durability: int
    max_dur: int
    name: str

    def restore(self):
        self.durability = self.max_dur
    
    @property
    def is_broken(self) -> bool:
        return self.durability <= 0
    
    @property
    def is_destroyed(self) -> bool:
        return self.durability <= -self.max_dur
    
    def __str__(self):
        return f"{self.name} {self.durability}/{self.max_dur}"
    

@dataclass
class ArmorStats(DurableItem):
    """Represents armor stats."""
    defense: int

@dataclass
class WeaponStats(DurableItem):
    """Represents weapon stats."""
    damage: str
    crit: Optional[str] = None

@dataclass
class ImplementStats(DurableItem):
    """Represents a magic implement."""
    pwr: int
    damage: str