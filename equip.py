from dataclasses import dataclass
from typing import Tuple

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
    

@dataclass
class ArmorStats(DurableItem):
    """Represents armor stats."""
    defense: int

    def __str__(self):
        return f"{self.name} (Def {self.defense} Dur {self.durability}/{self.max_dur})"

@dataclass
class WeaponStats(DurableItem):
    """Represents weapon stats."""
    damage: Tuple[int, int]

    def __str__(self):
        low, high = self.damage
        return f"{self.name} (Dmg {low}-{high} Dur {self.durability}/{self.max_dur})"

@dataclass
class ImplementStats(DurableItem):
    """Represents a magic implement."""
    pwr: int
    damage: Tuple[int, int]

    def __str__(self):
        low, high = self.damage
        return f"{self.name} (Pwr {self.pwr} Dmg {low}-{high} Dur {self.durability}/{self.max_dur}"
