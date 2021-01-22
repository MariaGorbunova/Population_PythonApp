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
        self.largest_indices = []
        self.median = []
        self.years = np.genfromtxt(YEARS_FILE, dtype=int, delimiter=',')
        if DEBUG:
            print(self.years)

        with open(COUNTRIES_FILE) as f:
            csv_reader = csv.reader(f, delimiter=',')
            self.countries = np.array([row for row in csv_reader])

            if DEBUG:
                print(self.countries)

        self.population = np.loadtxt(POPULATION_FILE, delimiter=',', dtype=np.int64)
        if DEBUG:
            print(self.population.shape)

        self.some_stats()

    def find_largest(self):
        self.largest_indices = self.population[:, -1].argsort()[::-1][:10]
        self.largest_indices = self.largest_indices[::-1] #reversing the order
        if DEBUG:
            for i in self.largest_indices:
                print(f"{self.countries[i]} population: {self.population[i, -1]:,}")

    def some_stats(self):
        if DEBUG:
            print("calculating.. median")
        self.median = np.median(self.population, axis=0)
        if DEBUG:
            print(self.median)


    def plot_trendCountries(self,idxs):
        if DEBUG:
            print("plot trend")
        plt.plot(self.years, self.median, "--r", label="Median")
        for i in idxs:
            plt.plot(self.years, self.population[i], label=self.countries[i][0])
        plt.legend(loc="best")
        plt.title("Population for selected countries")
        plt.ylabel("population, mln")
        plt.xticks(self.years, rotation=90)
        plt.show()



    def plot_regionTrend(self):
        print("Plotting region trend")

        return "Names of regions"



    def plot_growth(self):
        print("plot growth for top 10")

        country_name = [self.countries[i, 0] for i in self.largest_indices]
        country_pop = [self.population[i, -1] for i in self.largest_indices]

        plt.bar(country_name, country_pop, edgecolor='blue')
        plt.title("Top 10 in 2019")
        plt.ylabel("population, mln")
        plt.xticks(country_name, rotation=90)

        plt.show()
        return country_name





c = Countries()
c.find_largest()
#c.plot_trendCountries([6,14,100,66,34])
c.plot_growth()


