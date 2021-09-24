import tkinter as tk

from typing import Tuple, Optional, List
from character import Character, BaseStats
from charframe import CharFrame, create_int_label, create_label, create_str_label
from dataloader import GAME_DATA

class NewCharFrame(tk.Frame):
    """New Character Form."""

    def __init__(self, master, character: Character):
        super().__init__(master)
        self.character = character
        race_list = [race_data["name"] for race_data in GAME_DATA["races"].values()]
        list_var = tk.StringVar(value=race_list)
        self.race_combo = tk.Listbox(self, listvariable=list_var)
        self.race_combo.pack()
        


class CharGenFrame(tk.Toplevel):
    """Character Generation Window."""

    def __init__(self, master):
        super().__init__(master)
        self.character = Character("No Name", BaseStats())
        self.new_char_grid=NewCharFrame(self, self.character)
        self.char_frame = CharFrame(self, self.character)
        self.new_char_grid.grid(row=0, column=0)
        self.char_frame.grid(row=0, column=1)



