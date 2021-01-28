# Maria Gorbunova
# Assignment 2
'''lab1 has three classes for three different windows
with three options to plot data for world population'''

import tkinter as tk
import matplotlib

matplotlib.use('TkAgg')  # tell matplotlib to work with Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Canvas widget
import matplotlib.pyplot as plt  # normal import of pyplot to plot
from countries import Countries


class MainWin:
    def __init__(self, master):
        self.master = master
        self.data = Countries()
        self.master.geometry("400x100")
        self.master.title("Population")

        self.frame = tk.Frame(self.master)
        self.label = tk.Label(self.master, text="Population of Countries", fg="blue")
        self.label.pack()
        self.butnew("By Regions", "1", PlotWin)
        self.butnew("Top Ten", "2", PlotWin)
        self.butnew("By Countries", "3", DialogWin)
        self.frame.pack()

    def butnew(self, text, number, _class):
        '''creates a new button and sets a proper command to it'''
        tk.Button(self.frame, text=text, command=lambda: self.new_window(number, _class)).grid(row=1,
                                                                                               column=int(number))

    '''class UI:
        def __init__(self, fname =None):
            try:
                try:
                    self.data = Countries(fname)
                except TypeError:
                    self.data = Countries()

                self.regions = self.data.getRegions()
                self.incomeRank = self.data.getIncome()
            except IOError:
                raise SystemExit("file". fname, "not found")'''

    def new_window(self, number, _class):
        '''method to open a new window'''
        self.new = tk.Toplevel(self.master)
        _class(self.new, number, self.data)


class PlotWin:
    def __init__(self, master, number, data):

        self.master = master
        self.data = data
        fig = plt.figure(figsize=(6, 6))
        fig.add_subplot(111)

        if number == "1":
            self.data.plot_regionTrend()
        elif number == "2":
            self.data.plot_growth()
        else:
            self.data.plot_trendCountries(number)

        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.get_tk_widget().grid()
        canvas.draw()

    def close_window(self):
        '''closes the window'''
        self.master.destroy()


class DialogWin:
    def __init__(self,  master, number,  data):
        self.data = data
        self.master = master
        self.master.geometry("300x200")
        self.master.grab_set()
        self.master.focus_set()
        self.master.title("Choose countries")

        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.pack(side='right', fill='y')
        self.listbox = tk.Listbox(self.master, height=10, width=30, selectmode="multiple")
        self.listbox.insert(tk.END, *self.data.get_countries())
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.pack()

        self.idxs = []
        self.listbox.bind('<ButtonRelease-1>', self.on_click_listbox)
        self.butnew("Ok", PlotWin)

    def on_click_listbox(self, event):
        '''assignes ids for countries clicked by user'''
        self.idxs = list(self.listbox.curselection())

    def butnew(self, text, _class):
        '''new OK button to plot the picked values'''
        tk.Button(self.master, text=text, command=lambda: [self.new_window(_class), ]).pack()

    def new_window(self, _class):
        ''' create new window'''
        self.new = tk.Toplevel(self.master)
        _class(self.new, self.idxs, self.data)

    def close_window(self):
        '''closes the window'''
        self.master.destroy()

#driver
root = tk.Tk()
app = MainWin(root)
root.mainloop()
