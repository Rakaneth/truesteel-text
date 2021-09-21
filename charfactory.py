from character import Character, BaseStats
from dataloader import GAME_DATA

def build_char(race_id: str, class_id: str, name: str=None):
    class_data = GAME_DATA["classes"][class_id]
    race_data = GAME_DATA["races"][race_id]
    class_stats = class_data["stats"]
    race_stats = race_data["stats"]

    stats = BaseStats(
        strength=race_stats["str"],
        stamina=race_stats["stam"],
        speed=race_stats["spd"],
        skill=race_stats["skl"],
        sagacity=race_stats["sag"],
        smarts=race_stats["smt"],
        melee=race_stats["melee"],
        magic=race_stats["magic"]
    )

    class_mods = BaseStats(
        strength=class_stats.get("str", 0),
        stamina=class_stats.get("stam", 0),
        speed=class_stats.get("spd", 0),
        skill=class_stats.get("skl", 0),
        sagacity=class_stats.get("sag", 0),
        smarts=class_stats.get("smt", 0),
        melee=class_stats.get("melee", 0),
        magic=class_stats.get("magic", 0)
    )

    combined_stats = stats + class_mods
    base_name = f"{race_data['name']} {class_id}"
    
    if name:
        char_name = name
    else:
        char_name = base_name

    foetus = Character(char_name, combined_stats)
    foetus.stats.body = foetus.max_body
    foetus.stats.soul = foetus.max_soul
    foetus.stats.mind = foetus.max_mind

    return foetus


