import json
import tkinter as tk

from character import Character, BaseStats
from charframe import CharFrame
from charfactory import build_char
from equipfactory import make_armor, make_implement, make_weapon

def new_character():
    print("New Character selected")

def open_character():
    print("Open Character selected")

def exit_prog():
    raise SystemExit(0)

def main():
    root = tk.Tk()
    menubar = tk.Menu(root)
    sample_char = build_char("dwarf", "warlock")
    imp = make_implement("brass rod")
    armor = make_armor("padded")
    wpn = make_weapon("shortsword")
    sample_char.weapon = wpn
    sample_char.armor = armor
    sample_char.implement = imp
    charframe = CharFrame(root, sample_char)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="New Character", command=new_character)
    filemenu.add_command(label="Open Character", command=open_character)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=exit_prog)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)
    charframe.pack()
    root.wm_title("System 12 Arena")
    root.mainloop()

if __name__ == "__main__":
    main()