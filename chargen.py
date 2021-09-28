import tkinter as tk

from typing import Tuple, Optional, List
from character import Character, BaseStats
from charframe import CharFrame, create_int_label, create_label, create_str_label
from dataloader import GAME_DATA
from eventbus import MAIN_BUS

class NewCharFrame(tk.Frame):
    """New Character Form."""
    RACE_TO_BUILD = {v["name"]: k for k, v in GAME_DATA["races"].items()}

    def __init__(self, master, character: Character):
        super().__init__(master)
        self.character = character
        race_list = list(self.RACE_TO_BUILD.keys())
        list_var = tk.StringVar(value=race_list)
        self.race_combo = tk.Listbox(self, listvariable=list_var)
        self.race_combo.bind("<<ListboxSelect>>", self.update_race)
        self.race_combo.pack()
    
    def update_race(self, event):
        cur_value = self.race_combo.get(tk.ANCHOR)
        race_key = self.RACE_TO_BUILD[cur_value]
        race_data = GAME_DATA["races"][race_key]
        self.character.stats = BaseStats.from_dict(**race_data["stats"])
        MAIN_BUS.emit("charupdate")
        

class CharGenFrame(tk.Toplevel):
    """Character Generation Window."""

    def __init__(self, master):
        super().__init__(master)
        self.character = Character("No Name", BaseStats())
        self.new_char_grid=NewCharFrame(self, self.character)
        self.char_frame = CharFrame(self, self.character)
        self.new_char_grid.grid(row=0, column=0)
        self.char_frame.grid(row=0, column=1)
        MAIN_BUS.subscribe("charupdate", self)
    
    def on_charupdate(self):
        self.char_frame.refresh()



