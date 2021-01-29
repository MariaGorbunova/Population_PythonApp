# Maria Gorbunova
# Assignment 2
'''lab1 has three classes for three different windows
with three options to plot data for world population'''

import tkinter as tk
import matplotlib

matplotlib.use('TkAgg')  # tell matplotlib to work with Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Canvas widget
import tkinter.messagebox as tkmb
import matplotlib.pyplot as plt  # normal import of pyplot to plot
from population import Population


class MainWin(tk.Tk):
    def __init__(self, fname=None):
        super().__init__()
        self.fname = fname

        self.geometry("400x100")
        self.title("Population")
        self.frame = tk.Frame(self)
        self.label = tk.Label(self, text="Population of Countries", fg="blue")
        self.label.pack()

        try:
            try:
                self.data = Population(self.fname)
            except TypeError:
                self.data = Population()
            self.butnew("By Regions", "1", PlotWin)
            self.butnew("Top Ten", "2", PlotWin)
            self.butnew("By Countries", "3", DialogWin)
            self.frame.pack()
        except IOError:
            self.callback_fct()

    def callback_fct(self):
        '''open an error window for wrong file'''
        error_str = "[Errno 1]: No such file or directory:"+self.fname
        if tkmb.showerror("Error", error_str, parent=self):
            self.destroy()

    def butnew(self, text, number, _class):
        '''creates a new button and sets a proper command to it'''
        tk.Button(self.frame, text=text, command=lambda: self.new_window(number, _class)).grid(row=1,
                                                                                               column=int(number))

    def new_window(self, idx, _class):
        '''method to open a new window'''
        dialogWin = _class(idx, self.data)
        self.wait_window(dialogWin)
        if idx == "3" and len(dialogWin.get_idx()) != 0:
            self.new_window(dialogWin.get_idx(), PlotWin)


class PlotWin(tk.Toplevel):
    def __init__(self, idx, data):
        tk.Toplevel.__init__(self)
        self.data = data
        fig = plt.figure(figsize=(6, 6))
        fig.add_subplot(111)

        if idx == "1":
            self.title("Plot trends for regions")
            self.data.plot_regionTrend()
        elif idx == "2":
            self.title("Plot top 10 countries in 2019")
            self.data.plot_growth()
        else:
            self.title("Plot trends for selected countries")
            self.data.plot_trendCountries(idx)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()

    def close_window(self):
        '''closes the window'''
        self.destroy()


class DialogWin(tk.Toplevel):
    def __init__(self, number, data):
        tk.Toplevel.__init__(self)
        self.data = data
        self.geometry("300x200")
        self.grab_set()
        self.focus_set()
        self.title("Choose countries")

        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side='right', fill='y')
        self.listbox = tk.Listbox(self, height=10, width=30, selectmode="multiple")
        self.listbox.insert(tk.END, *self.data.get_countries())
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.pack()

        self.idxs = []
        self.listbox.bind('<ButtonRelease-1>', self.on_click_listbox)
        self.butnew("Ok", PlotWin)

    def on_click_listbox(self, event):
        '''assigns ids for countries clicked by user'''
        self.idxs = list(self.listbox.curselection())

    def butnew(self, text, _class):
        '''new OK button to plot the picked values'''
        tk.Button(self, text=text, command=lambda: [self.close_window()]).pack()

    def get_idx(self):
        '''getter for list of picked countries'''
        return self.idxs

    def close_window(self):
        '''closes the window'''
        self.destroy()


# driver
MainWin().mainloop()


#test error window
#MainWin("somefilename.csv").mainloop()