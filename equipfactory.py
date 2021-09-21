from dataloader import GAME_DATA
from equip import WeaponStats, ArmorStats, ImplementStats

def make_weapon(build_id: str) -> WeaponStats:
    weapon_data = GAME_DATA["weapons"][build_id]
    low, high = weapon_data["damage"]
    return WeaponStats(
        durability=weapon_data["durability"],
        max_dur=weapon_data["durability"],
        crit=weapon_data["crit"],
        damage=(low, high),
        name=weapon_data["name"]
    )

def make_armor(build_id: str) -> ArmorStats:
    armor_data = GAME_DATA["armor"][build_id]
    return ArmorStats(
        durability=armor_data["durability"],
        max_dur=armor_data["durability"],
        defense=armor_data["defense"],
        name=armor_data["name"]
    )

def make_implement(build_id: str) -> ImplementStats:
    imp_data = GAME_DATA["implements"][build_id]
    low, high = imp_data["damage"]
    return ImplementStats(
        durability=imp_data["durability"],
        max_dur=imp_data["durability"],
        damage = (low, high),
        name=imp_data["name"],
        pwr=imp_data["pwr"]
    )
