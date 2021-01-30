# Maria Gorbunova
# Assignment 2
'''lab1 has three classes for different windows
with three options to plot data for world population'''

import tkinter as tk
import matplotlib

matplotlib.use('TkAgg')  # tell matplotlib to work with Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Canvas widget
import tkinter.messagebox as tkmb  # open error message if no file exception
import matplotlib.pyplot as plt  # normal import of pyplot to plot
from population import Population


class MainWin(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__()
        self.geometry("400x100")
        self.title("Population")
        self.frame = tk.Frame(self)
        self.label = tk.Label(self, text="Population of Countries", fg="blue")
        self.label.pack()

        try:
            try:
                self.data = Population(**kwargs)
            except TypeError:
                self.data = Population()
            self.butnew("By Regions", "1", PlotWin)
            self.butnew("Top Ten", "2", PlotWin)
            self.butnew("By Countries", "3", DialogWin)
            self.frame.pack()
            self.protocol("WM_DELETE_WINDOW", self.exit_fct)
        except Exception as e:
            self.error_fct(str(e))

    def exit_fct(self):
        self.destroy()
        raise SystemExit("Terminated the program")

    def error_fct(self, errmessage):
        '''open an error window for the wrong file'''
        error_str = "[Errno 1]: " + errmessage
        if tkmb.showerror("Error", error_str, parent=self):
            self.destroy()
            # decided to not do it since the program closes and stops automatically
            # self.exit_fct()
            # OR
            # raise SystemExit('Exited the program')

    def butnew(self, text, number, _class):
        '''creates a new button and sets a proper command to it based on a number values passed here'''
        tk.Button(self.frame, text=text, command=lambda: self.new_window(number, _class)).grid(row=1,
                                                                                               column=int(number))

    def new_window(self, idx, _class):
        '''method to open a new window,
        if it is a dialog window, waits for it to be closed,
         then opens another one after getting indexes from it'''
        dialogWin = _class(self, idx, self.data)
        self.wait_window(dialogWin)
        if idx == "3" and dialogWin.boolPlot():
            self.new_window(dialogWin.get_idx(), PlotWin)


class PlotWin(tk.Toplevel):
    def __init__(self, master, idx, data):
        super().__init__(master)

        # old version. Changed it so it is like in class notes
        # tk.Toplevel.__init__(self)
        self.data = data
        fig = plt.figure(figsize=(7, 7))
        fig.add_subplot(111)

        #Note to myself: maybe use switch stmt?
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


class DialogWin(tk.Toplevel):
    def __init__(self, master, number, data):
        super().__init__(master)

        # old version. Changed it so it is like in class notes
        # tk.Toplevel.__init__(self)
        self.data = data
        self.geometry("300x200")
        self.grab_set()
        self.focus_set()
        self.title("Choose countries")

        # creating the scrollbar and listbox here
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side='right', fill='y')
        self.listbox = tk.Listbox(self, height=10, width=30, selectmode="multiple")
        self.listbox.insert(tk.END, *self.data.get_countries())
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.pack()

        self.idxs = []
        self.shouldPlot = False
        self.listbox.bind('<ButtonRelease-1>', self.on_click_listbox)
        self.butnew("Ok")

    def on_click_listbox(self, event):
        '''assigns ids for countries clicked by user'''
        self.idxs = list(self.listbox.curselection())

    def butnew(self, text):
        '''new OK button to plot the picked values'''
        tk.Button(self, text=text, command=lambda: self.close_window()).pack()

    def boolPlot(self):
        '''getter for the plotting bool value'''
        return self.shouldPlot

    def get_idx(self):
        '''getter for list of picked countries'''
        return self.idxs

    def close_window(self):
        '''closes the window and sets the bool so it allows to create the plot window'''
        self.shouldPlot = True
        self.destroy()


# driver
MainWin().mainloop()

# TESTING ERROR WINDOW with various filenames
# MainWin(years = "somefilename.csv", countries = "somefilename1.csv",  population ="somefilename2.csv").mainloop()
# MainWin(years = 'years.csv', countries = "somefilename1.csv",  population ="somefilename2.csv").mainloop()
# MainWin(years = 'years.csv', population = 'population.csv').mainloop()
# MainWin(  "somefilename2.csv", years = 'years.csv', countries = "somefilename1.csv",  population ="somefilename2.csv").mainloop()

#this line will give type error: three positional args were given, 1 expected
#MainWin( 'years.csv',  "somefilename1.csv",  population ="somefilename2.csv").mainloop()

# this will work but will give weird data
#MainWin(years = 'years.csv', countries = 'population.csv').mainloop() #this might work but will give weird values

'''EC
East Asia and South Asia have the highest population growth. 
This is because India and China are in those regions and they have two
of the largest populations. 

'''
