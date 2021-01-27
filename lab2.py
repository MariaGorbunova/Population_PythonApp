# Maria Gorbunova
# Assignment 2

import tkinter as tk
import matplotlib

matplotlib.use('TkAgg')  # tell matplotlib to work with Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Canvas widget
import matplotlib.pyplot as plt  # normal import of pyplot to plot
from countries import Countries


class MainWin:
    def __init__(self, master):
        self.master = master
        self.data = self.getData()
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

    def getData(self):
        return Countries()

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
        self.new = tk.Toplevel(self.master)
        _class(self.new, number, self.data)


class PlotWin:
    def __init__(self, master, number, data):

        self.master = master
        self.data = data
        fig = plt.figure(figsize=(6, 6))
        fig.add_subplot(111)

        if int(number) == 1:
            self.data.plot_regionTrend()
        elif int(number) == 2:
            self.data.plot_growth()
        else:
            self.data.plot_trendCountries(number)

        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.get_tk_widget().grid()
        canvas.draw()

    def close_window(self):
        self.master.destroy()


class Win3:
    def __init__(self, master, number, data):
        self.data = data
        self.master = master
        self.master.geometry("400x400+200+200")
        self.S = tk.Scrollbar(master)
        self.LB = tk.Listbox(master, height=600, width=600, selectmode="multiple", yscrollcommand=self.S.set)
        self.S.config(command=self.LB.yview)
        self.LB.insert(tk.END, *self.data.get_countries())
        idx = self.LB.curselection()
        self.LB.pack()
        self.S.pack()



    def close_window(self):
        self.master.destroy()


root = tk.Tk()
app = MainWin(root)
root.mainloop()
