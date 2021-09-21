from character import BaseStats, Effect, Character, DamageType
from random import randint

class Damage(Effect):
    """
    Describes an immediate instant damage effect.
    Used by spells and crit effects.
    """
    def __init__(self, low: int, high: int, dtype: DamageType):
        super().__init__("damage", Effect.IMMEDIATE, 0)
        self.potency = randint(low, high)
        self.type = dtype
    
    def on_apply(self, bearer: Character):
        if self.type == DamageType.BODY:
            bearer.body -= self.potency
        elif self.type == DamageType.MIND:
            bearer.mind -= self.potency
        elif self.type == DamageType.SOUL:
            bearer.soul -= self.potency

class DOT(Effect):
    """
    Describes any kind of DoT effect.
    This is an abstract class.
    """

    def __init__(self, name: str, duration: int, potency: int, dtype: DamageType):
        super().__init__(name, duration, potency)
        self.type = dtype
    
    def on_tick(self, bearer: Character):
        if self.type == DamageType.BODY:
            bearer.body -= self.potency
        elif self.type == DamageType.MIND:
            bearer.mind -= self.potency
        elif self.type == DamageType.SOUL:
            bearer.soul -= self.potency

class Burn(DOT):
    """
    Describes a burning effect.
    Burning does 3 BODY damage per tick. 
    Stacks duration.
    Generally caused by magical effects.
    """

    def __init__(self, duration: int):
        super().__init__("Burning", duration, 3, DamageType.BODY)
    
    def on_merge(self, eff: Effect):
        self.duration += eff.duration

class Bleed(DOT):
    """
    Describes a bleeding effect.
    Bleeding does 1 BODY damage per tick.
    Stacks intensity, refreshes duration.
    Generally caused by big attacks.
    """

    def __init__(self, duration: int):
        super().__init__("Bleeding", duration, 1, DamageType.BODY)
    
    def on_merge(self, eff: Effect):
        self.duration = eff.duration
        self.potency += 1
    
class StatChange(Effect):
    """
    Describes an effect that alters stats.
    Refreshes duration.
    This is an abstract class.
    """

    def __init__(
        self, name: str,
        duration: int, 
        orig_stats: BaseStats,
        new_stats: BaseStats
    ):
        super().__init__(name, duration, 0)
        self.orig_stats = orig_stats
        self.new_stats = new_stats
    
    def on_remove(self, bearer: Character):
        bearer.stats = self.orig_stats
    
    def on_apply(self, bearer: Character):
        bearer.stats += self.new_stats


class Might(StatChange):
    """
    Describes a Might effect.
    The Might effect buffs STR and STAM by 10.
    Generally caused by magic or creature skills.
    """
    
    def __init__(self, duration: int, base_stats: BaseStats):
        super().__init__(
            "Might", 
            duration, 
            base_stats,
            BaseStats(strength=10, stamina=10)
        )

class Weakness(StatChange):
    """
    Describes a Weakness effect.
    The Weakness effect debuffs STR and STAM by 10.
    Generally caused by magic or creature skills.
    """
    def __init__(self, duration: int, base_stats: BaseStats):
        super().__init__(
            "Weakness",
            duration,
            base_stats,
            BaseStats(strength=-10, stamina=-10)
        )






    

