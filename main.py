import tkinter as tk

from character import Character, BaseStats
from charframe import CharFrame
from chargen import CharGenFrame
from charfactory import build_char
from equipfactory import make_armor, make_implement, make_weapon

def main():
    root = tk.Tk()
    menubar = tk.Menu(root)
    chargen = None
    
    def new_character():
        nonlocal chargen
        if chargen is None:
            chargen = CharGenFrame(root)
    
    def open_character():
        pass

    def exit_prog():
        raise SystemExit(0)
    
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="New Character", command=new_character)
    filemenu.add_command(label="Open Character", command=open_character)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=exit_prog)
    menubar.add_cascade(label="File", menu=filemenu)

    root.config(menu=menubar)
    root.wm_title("System 12 Arena")
    root.mainloop()

if __name__ == "__main__":
    main()