from character import Character, BaseStats
from tkinter import Frame, Label, IntVar, StringVar
from typing import Tuple

def create_label(master, caption: str, row: int, column: int, width: int=8) -> Label:
    l = Label(master, text=caption, anchor='e', width=width)
    l.grid(row=row, column=column)
    return l

def create_int_label(master, row: int, column: int, init_value=0) -> Tuple[Label, IntVar]:
    v = IntVar(value=init_value)
    l = Label(master, textvariable=v)
    l.grid(row=row, column=column)
    return (l, v)

def create_str_label(master, row: int, column: int, init_value=None) -> Tuple[Label, StringVar]:
    v = StringVar(value=init_value)
    l = Label(master, textvariable=v)
    l.grid(row=row, column=column)
    return (l, v)

class CharBasedFrame(Frame):
    """Base abstract class for a frame displaying character info."""

    def __init__(self, master, character: Character):
        super().__init__(master, relief='sunken', borderwidth=1, padx=3, pady=3)
        self.character = character
    
    def refresh(self):
        """Refreshes labels on change."""
        pass

class StatFrame(CharBasedFrame):
    """Displays a set of base stats."""
    def __init__(self, master, stats: BaseStats):
        super().__init__(master, None)
        self.stats = stats
        self.str_caption = create_label(self, "Strength", 1, 0)
        self.str_label, self.str_value = create_int_label(self, 1, 1, self.stats.strength)

        self.stam_caption = create_label(self, "Stamina", 2, 0)
        self.stam_label, self.stam_value = create_int_label(self, 2, 1, self.stats.stamina)

        self.spd_caption = create_label(self, "Speed", 3, 0)
        self.spd_label, self.spd_value = create_int_label(self, 3, 1, self.stats.speed)

        self.skl_caption = create_label(self, "Skill", 4, 0)
        self.skl_label, self.skl_value = create_int_label(self, 4, 1, self.stats.skill)

        self.sag_caption = create_label(self, "Sagacity", 5, 0)
        self.sag_label, self.sag_value = create_int_label(self, 5, 1, self.stats.sagacity)

        self.smt_caption = create_label(self, "Smarts", 6, 0)
        self.smt_label, self.smt_value = create_int_label(self, 6, 1, self.stats.smarts)

        self.melee_caption = create_label(self, "Melee", 7, 0)
        self.melee_label, self.melee_value = create_int_label(self, 7, 1, self.stats.melee)

        self.magic_caption = create_label(self, "Magic", 8, 0)
        self.magic_label, self.magic_value = create_int_label(self, 8, 1, self.stats.magic)

    def refresh(self):
        self.str_value.set(self.stats.strength)
        self.stam_value.set(self.stats.stamina)
        self.spd_value.set(self.stats.speed)
        self.skl_value.set(self.stats.skill)
        self.sag_value.set(self.stats.sagacity)
        self.smt_value.set(self.stats.smarts)

class DerivedStatFrame(CharBasedFrame):
    """Displays a set of derived stats."""

    def __init__(self, master, character: Character):
        super().__init__(master, character)
        
        self.atp_caption = create_label(self, "ATP", 0, 0, 3)
        self.atp_label, self.atp_value = create_int_label(self, 0, 1, self.character.atp)

        self.dfp_caption = create_label(self, "DFP", 1, 0, 3)
        self.dfp_label, self.dfp_value = create_int_label(self, 1, 1, self.character.dfp)

        self.tou_caption = create_label(self, "TOU", 2, 0, 3)
        self.tou_label, self.tou_value = create_int_label(self, 2, 1, self.character.tou)

        self.wil_caption = create_label(self, "WIL", 3, 0, 3)
        self.wil_label, self.wil_value = create_int_label(self, 3, 1, self.character.wil)

        self.pwr_caption = create_label(self, "PWR", 4, 0, 3)
        self.pwr_label, self.pwr_value = create_int_label(self, 4, 1, self.character.pwr)

    def refresh(self):
        self.atp_value.set(self.character.atp)
        self.dfp_value.set(self.character.dfp)
        self.tou_value.set(self.character.tou)
        self.wil_value.set(self.character.wil)
        self.pwr_value.set(self.character.pwr)

class VitalsFrame(CharBasedFrame):
    """Displays a character's vitals."""
    
    def __init__(self, master, character: Character):
        super().__init__(master, character)
        
        self.body_caption = create_label(self, "Body", 0, 0, 4)
        self.body_label, self.body_val = create_str_label(self, 0, 1, self.character.body_string)
        
        self.mind_caption = create_label(self, "Mind", 1, 0, 4)
        self.mind_label, self.mind_val = create_str_label(self, 1, 1, self.character.mind_string)

        self.soul_caption = create_label(self, "Soul", 2, 0, 4)
        self.soul_label, self.soul_val = create_str_label(self, 2, 1, self.character.soul_string)
    
    def refresh(self):
        self.soul_val.set(self.character.soul_string)
        self.mind_val.set(self.character.mind_string)
        self.body_val.set(self.character.body_string)

class EquipFrame(CharBasedFrame):
    """Displays equipment information."""

    def __init__(self, master, character: Character):
        super().__init__(master, character)

        self.weapon_caption = create_label(self, "Weapon", 0, 0, 9)
        self.weapon_label, self.weapon_val = create_str_label(
            self, 0, 1, self.character.weapon_string
        )
        
        self.armor_caption = create_label(self, "Armor", 1, 0, 9)
        self.armor_label, self.armor_val = create_str_label(
            self, 1, 1, self.character.armor_string
        )

        self.implement_caption = create_label(self, "Implement", 2, 0, 9)
        self.implement_label, self.implement_val = create_str_label(
            self, 2, 1, self.character.implement_string
        )

    def refresh(self):
        self.weapon_val.set(self.character.weapon_string)
        self.armor_val.set(self.character.armor_string)
        self.implement_val.set(self.character.implement_string)


class CharFrame(Frame):
    """Displays character info."""

    def __init__(self, master, character: Character):
        super().__init__(master, relief='raised', borderwidth=3)
        self.character = character
        
        name_label = Label(self, text=character.name)
        name_label.grid(column=0, row=0, columnspan=2)
        
        self.stat_frame = StatFrame(self, self.character.stats)
        self.stat_frame.grid(row=1, column=0)
        
        self.dstat_frame = DerivedStatFrame(self, self.character)
        self.dstat_frame.grid(row=1, column=1, sticky='n')

        self.vitals_frame = VitalsFrame(self, self.character)
        self.vitals_frame.grid(row=1, column=1, sticky='s')

        self.eq_frame = EquipFrame(self, self.character)
        self.eq_frame.grid(row=1, column=2, sticky='n')
    
    def refresh(self):
        """Refreshes all the child frames."""
        frames = (self.stat_frame, self.dstat_frame, self.vitals_frame, self.eq_frame)
        for frame in frames:
            frame.refresh()




        

    


