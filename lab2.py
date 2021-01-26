# Maria Gorbunova
# Assignment 2

import tkinter as tk
from countries import Countries


class MainWin:
    def __init__(self, master):
        self.master = master

        self.master.c = Countries()

        self.master.geometry("400x100")
        self.master.title("Population")

        self.frame = tk.Frame(self.master)
        self.label = tk.Label(self.master, text="Population of Countries", fg="blue")
        self.label.pack()
        self.butnew("By Regions", "1", PlotWin)
        self.butnew("Top Ten", "2", PlotWin)
        self.butnew("By Countries", "3", Win3)
        self.frame.pack()

    def butnew(self, text, number, _class):
        tk.Button(self.frame, text=text, command=lambda: self.new_window(number, _class)).grid(row=1,
                                                                                               column=int(number))

    def new_window(self, number, _class):
        self.new = tk.Toplevel(self.master)
        _class(self.new, number)


class PlotWin:
    def __init__(self, master, number):
        self.master = master
        self.master.geometry("400x400+200+200")
        self.frame = tk.Frame(self.master)


        self.frame.pack()

    def close_window(self):
        self.master.destroy()


class Win3:
    def __init__(self, master, number):
        self.master = master
        self.master.geometry("400x400+200+200")
        self.frame = tk.Frame(self.master)
        self.quit = tk.Button(self.frame, text=f"Quit this window n. {number}", command=self.close_window)
        self.quit.pack()
        self.label = tk.Label(self.frame, text="THIS IS ONLY IN THE THIRD WINDOW")
        self.label.pack()
        self.frame.pack()

    def close_window(self):
        self.master.destroy()


root = tk.Tk()
app = MainWin(root)
root.mainloop()
