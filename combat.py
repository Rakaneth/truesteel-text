import re

from character import Character, DamageType, Effect
from typing import List, Optional, Tuple
from collections import namedtuple
from random import randint


RollResult = namedtuple('RollResult', ('roll', 'target', 'success', 'threshold', 'crit'))
DICE_PATTERN = re.compile(r"(?P<num>\d+)d(?P<sides>\d+)(?:(?P<num_bonus>(?:\+|\-)\d+))?(?:\+(?P<stat_bonus>imp|strmod|sklmod))?")

class BadStatError(Exception):
    """Custom exception for bad stats passed to `attack`."""
    pass

class BadDiceError(Exception):
    """Custom exception for bad dice passed to `dice_str`. """
    def __init__(self, bad_str: str):
        super().__init__(f"{bad_str} is not a valid dice string.")

def dice(sides: int, num: int=1, bonus=0) -> int:
    """
    Rolls `num`d`sides`+`bonus`. 
    `num` defaults to 1.
    `bonus` defaults to 0.
    """
    acc = 0
    for _ in range(num):
        acc += randint(1, sides)
    
    return acc + bonus

def dice_str(d_str: str) -> int:
    """
    Parses `d_str` in standard dice notation and rolls the result.
    Discards character values like +IMP or +STRMOD.
    Used primarily for rolling weapon damage.
    """
    dice_match = DICE_PATTERN.match(d_str)
    if not dice_match:
        raise BadDiceError(d_str)
    
    num = int(dice_match.group("num"))
    sides = int(dice_match.group("sides"))
    bonus_str = dice_match.groupdict().get("num_bonus", None)
    bonus = 0

    if bonus_str:
        bonus = int(dice_match.group("num_bonus"))
    
    return dice(sides, num, bonus)

def d100() -> int:
    """Convenience method for rolling a d100. Most rolls in the combat system are d100s."""
    return dice(100)

def apply_effect(victim: Character, eff: Effect):
    maybe_eff = victim.find_effect(eff.name)
    if maybe_eff:
        maybe_eff.on_merge(eff)
    else:
        victim.effects.add(eff)
        eff.on_apply(victim)

def remove_effect(victim: Character, eff: Effect, raw=False):
    """
    Removes `eff` from `victim`.
    Applies `eff.on_remove` effects by default. 
    Pass `raw=True` to avoid processing `on_remove`.
    """
    if not raw:
        eff.on_remove(victim)
    victim.effects.remove(eff)

def tick_effects(victim: Character):
    """Ticks all effects on `victim` and removes them if their durations are 0 or less."""
    to_remove: List[Effect] = []
    for eff in victim.effects:
        eff.duration -= 1
        eff.on_tick(victim)
        if eff.duration <= 0:
            to_remove.append(eff)
    
    for done_effect in to_remove:
        remove_effect(done_effect, victim)

def hit(attacker: Character, defender: Character, atk_stat: str, def_stat: str) -> RollResult:
    if atk_stat == "atp":
        atk_bonus = attacker.atp
    elif atk_stat == "pwr":
        atk_bonus = attacker.pwr
    else:
        raise BadStatError(f"{atk_stat} is not a valid attack stat")
    
    if def_stat == "dfp":
        def_bonus = defender.dfp
    elif def_stat == "tou":
        def_bonus = defender.tou
    elif def_stat == "wil":
        def_bonus = defender.wil
    else:
        raise BadStatError(f"{def_stat} is not a valid defense stat")
    
    raw_roll = d100()
    atk_roll = atk_bonus + raw_roll
    success = (atk_roll >= def_bonus)
    threshold = atk_roll - def_bonus
    crit = (threshold >= 50 or raw_roll >= 95)

    return RollResult(
        roll=atk_roll, 
        target=def_bonus, 
        success=success,
        threshold=threshold,
        crit=crit
    )

def damage(victim: Character, amt: int, dtype: DamageType, armor_ok=True, shield_ok=True):
    #All damage tries to go to shield first
    maybe_shield = victim.find_effect("Shield")
    if maybe_shield and maybe_shield.potency > 0 and shield_ok:
        remainder = amt - maybe_shield.potency
        maybe_shield.potency = -remainder

        #Shield is broken at pot 0
        if maybe_shield.potency <= 0:
            remove_effect(victim, maybe_shield)
    else:
        remainder = amt
    
    #Damage is reduced by armor if it can be
    maybe_armor = victim.armor
    if maybe_armor and armor_ok:
        #If the attack doesn't go through armor, it damages broken armor
        if maybe_armor.is_broken:
           maybe_armor.durability -= 2
        else:
            #Damage is reduced by armor. if fully stopped, less armor damage.
            remainder -= maybe_armor.defense
            if remainder <= 0:
                maybe_armor.durability -= 1
            else:
                maybe_armor.durability -= 2
    
    #Remaining damage goes to the correct vital
    if remainder > 0:
        if dtype == DamageType.BODY:
            victim.body -= remainder
        elif dtype == DamageType.MIND:
            victim.mind -= remainder
        elif dtype == DamageType.SOUL:
            victim.soul -= remainder

    