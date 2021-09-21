import tkinter as tk
import json

from typing import Tuple, Optional, List
from character import Character, BaseStats
from charframe import CharFrame, create_int_label, create_label, create_str_label




class CharGenFrame(tk.Toplevel):
    """Character Generation Window."""

    def __init__(self, master):
        super().__init__(master)
        self.character = Character("No Name", BaseStats())
        self.char_frame = CharFrame(self, self.character)


