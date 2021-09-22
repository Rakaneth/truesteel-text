from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple, Optional, List, Set
from equip import WeaponStats, ArmorStats, ImplementStats
from enum import Enum, auto

class DamageType(Enum):
    BODY = auto()
    MIND = auto()
    SOUL = auto()

class Effect:
    """
    Describes a game effect. Effects have four lifecycle functions
    that are called at appropriate times and specific effects should override them:

    * `on_apply` occurs when a character receives the effect.
    * `on_tick` occurs each combat turn.
    * `on_merge` occurs when a character receives another copy of the same effect.
    By default, the current effect is retained with the duration of the incoming copy.
    * `on_remove` occurs when a character loses this effect, either through its duration
    expiring or through some combat action removing it.

    This is an abstract class.
    """
    IMMEDIATE: int = -1
    
    def __init__(self, name: str, duration: int, potency: int):
        """
        Game effects can be described and operated on in terms of their `potency` and `duration`. The effect's `name` should be unique.
        """
        self.name = name
        self.duration = duration
        self.potency = potency
    
    def on_remove(self, bearer: Character):
        """Triggers when an effect is removed from `bearer`."""
        pass
    
    def on_merge(self, eff: Effect):
        """
        Handles merges of `eff.`
        Effects refresh duration by default.
        """
        self.duration = eff.duration
    
    def on_tick(self, bearer: Character):
        """Triggers every turn for `bearer`."""
        pass
    
    def on_apply(self, bearer: Character):
        """Triggers when an effect is applied."""
        pass

@dataclass
class BaseStats:
    """Represents base stats of an actor."""
    strength: int = 0
    stamina: int = 0
    speed: int = 0
    skill: int = 0
    sagacity: int = 0
    smarts: int = 0
    melee: int = 0
    magic: int = 0
    body: int = 0
    mind: int = 0
    soul: int = 0

    def __add__(self, other: BaseStats):
        return BaseStats(
            self.strength + other.strength,
            self.stamina + other.stamina,
            self.speed + other.speed,
            self.skill + other.skill,
            self.sagacity + other.sagacity,
            self.smarts + other.smarts,
            self.melee + other.melee,
            self.magic + other.magic,
            self.body,
            self.mind,
            self.soul
        )

@dataclass
class Character:
    """Represents an animate actor in the world."""
    name: str
    stats: BaseStats
    weapon: Optional[WeaponStats] = None
    armor: Optional[ArmorStats] = None
    implement: Optional[ImplementStats] = None
    sort_index: int = field(repr=False, init=False)
    effects: Set[Effect] = field(repr=False, init=False)

    def __post_init__(self):
        self.sort_index = self.stats.speed
        self.stats.body = self.max_body
        self.stats.soul = self.max_soul
        self.stats.mind = self.max_mind
        self.effects = set()

    @property
    def strength(self) -> int:
        return self.stats.strength
    
    @property
    def stamina(self) -> int:
        return self.stats.stamina
    
    @property
    def speed(self) -> int:
        return self.stats.speed
    
    @property
    def skill(self) -> int:
        return self.stats.skill
    
    @property
    def sagacity(self) -> int:
        return self.stats.sagacity
    
    @property
    def smarts(self) -> int:
        return self.stats.smarts
    
    @property
    def atp(self) -> int:
        return self.stats.melee + self.stats.skill
    
    @property
    def dfp(self) -> int:
        return self.stats.skill + max(self.stats.magic, self.stats.melee)
    
    @property
    def tou(self) -> int:
        return self.stats.stamina + 50
    
    @property
    def wil(self) -> int:
        return self.stats.sagacity + 50
    
    @property
    def pwr(self) -> int:
        stat = self.stats.sagacity // 2 + self.stats.smarts // 2
        wpn = self.implement.pwr if self.implement else 0
        return stat + wpn + self.stats.magic
    
    @property
    def defense(self) -> int:
        return self.armor.defense if self.armor else 0
    
    @property
    def damage(self) -> Tuple[int, int]:
        return self.weapon.damage if self.weapon else (1, 1)
    
    @property
    def body(self) -> int:
        return self.stats.body
    
    @body.setter
    def body(self, val: int):
        self.stats.body = sorted(0, val, self.max_body)[1]
    
    @property
    def mind(self) -> int:
        return self.stats.mind
    
    @mind.setter
    def mind(self, val: int):
        self.stats.mind = sorted(0, val, self.max_mind)[1]
    
    @property
    def soul(self) -> int:
        return self.stats.soul
    
    @soul.setter
    def soul(self, val: int):
        self.stats.soul = sorted(0, val, self.max_soul)[1]
    
    @property
    def alive(self) -> bool:
        return self.body > 0 and self.soul > 0
    
    @property
    def str_mod(self) -> int:
        return self.strength // 10
    
    @property
    def stam_mod(self) -> int:
        return self.stamina // 10

    @property
    def skl_mod(self) -> int:
        return self.skill // 10
    
    @property
    def spd_mod(self) -> int:
        return self.speed // 10
    
    @property
    def sag_mod(self) -> int:
        return self.sagacity // 10
    
    @property
    def smt_mod(self) -> int:
        return self.smarts // 10
    
    @property
    def max_body(self) -> int:
        return self.stam_mod*5 + self.str_mod*2
    
    @property
    def max_mind(self) -> int:
        return self.sag_mod*5 + self.smt_mod*2
    
    @property
    def max_soul(self) -> int:
        return (
            self.str_mod + self.stam_mod +
            self.spd_mod + self.skl_mod + 
            self.sag_mod + self.smt_mod) * 3
    
    @property
    def body_string(self) -> str:
        return f"{self.body}/{self.max_body}"
    
    @property
    def mind_string(self) -> str:
        return f"{self.mind}/{self.max_mind}"
    
    @property
    def soul_string(self) -> str:
        return f"{self.soul}/{self.max_soul}"
    
    @property
    def weapon_string(self) -> str:
        if self.weapon:
            return f"{self.weapon}"
        
        return "Fists (Dmg 1-1)"
    
    @property
    def armor_string(self) -> str:
        if self.armor:
            return f"{self.armor}"
        
        return "None"
    
    @property
    def implement_string(self) -> str:
        if self.implement:
            return f"{self.implement}"
        
        return "None"
    
    def tick_effects(self):
        """
        Ticks all of the character's effects.
        Removes effects that have run out.
        """
        to_remove: List[Effect] = []
        for eff in self.effects:
            eff.on_tick(self)
            if eff.duration <= 0:
                to_remove.append(eff)
        
        for done in to_remove:
            self.remove_effect(done)

    def find_effect(self, eff_name: str) -> Optional[Effect]:
        """
        Finds an effect named `eff_name` in the character's effect list.
        Returns `None` if not found.
        """
        effs = [eff for eff in self.effects if eff.name == eff_name]
        if len(effs) == 0:
            return None
        
        return effs[0]




