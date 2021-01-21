import csv
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt


from collections import defaultdict

POPULATION_FILE = 'population.csv'
YEARS_FILE = 'years.csv'
COUNTRIES_FILE = 'countries.csv'

DEBUG = True


class Countries:

    def __init__(self):
        self.years = np.genfromtxt(YEARS_FILE, dtype=int, delimiter=',')
        if DEBUG:
            print(self.years)

        with open(COUNTRIES_FILE) as f:
            csv_reader = csv.reader(f, delimiter=',')
            self.countries = np.array([row for row in csv_reader])
            if DEBUG:
                print(self.countries)

        self.population = np.loadtxt(POPULATION_FILE , delimiter=',', dtype=np.int64)
        if DEBUG:
            print(self.population.shape)

    def find_largest(self):
        ind = np.argsort(self.population[:, -1])
        largest_indices = ind[::-1][:10]
        if DEBUG:
            for i in largest_indices:
                print(f"{self.countries[i]} population: {self.population[i, -1]:,}")

    def some_stats(self):

        print("calculating.. median")


    def plot_trendCountries(self,idxs):

        print("plot trend")
        



        '''
The plot method accepts a list of indices, each index is the index of a
country in the list of countries.
From the list of indices, find each corresponding country and plot the 
population of that country for all the years.
Also plot the median population of all the countries in the world, 
for all the years. This helps the user visually compare the population 
of their chosen countries and the median of all countries.
The plot must have: a title, a legend that shows the country names, 
the x-ticks should be the years,  a y-axis label, which is the population in millions.  
        '''

    def plot_regionTrend(self):
        print("Plotting region trend")


    def plot_growth(self):
        print("plot growth for top 10")





c = Countries()
c.find_largest()

