# Maria Gorbunova
# Assignment 2
'''countries has Countries class with all the backend of the program.
It has data for population and it plots the requested graphs'''
import numpy as np
import matplotlib.pyplot as plt

POPULATION_FILE = 'population.csv'
YEARS_FILE = 'years.csv'
COUNTRIES_FILE = 'countries.csv'

DEBUG = False

def print_return(foo):
    '''decorator to print return value for some methods in countries'''
    def wrapper(*args, **kwargs):
        result = foo(*args, **kwargs)
        for item in result:
            print(item)
        # return result
    return wrapper


class Population:
    ### how to deal with three default files???
    def __init__(self, years=YEARS_FILE, countries=COUNTRIES_FILE, population=POPULATION_FILE):
        # getting years from file
        self.years = np.genfromtxt(years, delimiter=',', dtype=int)
        if DEBUG:
            print(self.years)
        # getting countries from file
        self.countries = np.genfromtxt(countries, delimiter=',', dtype=str)
        if DEBUG:
            print(self.countries)
        # getting population data (2d array countries\years) from file
        self.population = np.loadtxt(population, delimiter=',', dtype=np.int64)
        if DEBUG:
            print(self.population.shape)
        # concatinating country names and populations in one numpy 2d array
        self.data = np.concatenate((self.countries[:, [0, 2]], self.population), axis=1)
        if DEBUG:
            print(self.data)
        # creating class variables: largest 10 countries and median
        self.largest_indices = self.find_largest()
        self.median = self.some_stats()

    def get_countries(self):
        '''returns a list of countries(names)'''
        return self.data[:, 0]

    def find_largest(self):
        '''returns idices of the top 10 largest populations'''

        ### is there a way to reverse it better? :-10?

        large_idx = self.population[:, -1].argsort()[::-1][:10]
        large_idx = large_idx[::-1]  # reversing the order


        if DEBUG:
            for i in self.largest_indices:
                print(f"{self.countries[i]} population: {self.population[i, -1]:,}")
        return large_idx

    def some_stats(self):
        '''calculates median, returns median'''
        # used population numpy array in order to not deal with text columns in self.data
        median = np.median(self.population, axis=0)
        if DEBUG:
            print("Calculating median")
            print(median)
        return median

    def plot_trendCountries(self, idxs):
        '''plotting population growth trend for selected countries'''
        if DEBUG:
            print("plot trend")
        plt.plot(self.years, self.median, "--r", label="Median")
        for i in idxs:
            plt.plot(self.years, self.population[i], label=self.countries[i][0]) ### fix y and x ticks
        plt.legend(loc="best")
        plt.title("Population for selected countries")
        plt.ylabel("population, mln")
        plt.xticks(self.years, rotation=90)

        # plt.show()

    '''This method was modified with the assistance of my classmate Ben.'''

    @print_return
    def plot_regionTrend(self):
        '''plot_regionTrend creates a plot with regions' population data'''
        if DEBUG:
            print("Plotting region trend")
        sorted_regions = sorted(set(self.data[:, 1]))
        for region in sorted_regions:
            region_arr = np.sum(self.population[self.data[:, 1] == region], 0)
            plt.plot(self.years, region_arr, label=region) ### fix y and x ticks

        plt.title("Total population for each region")
        plt.legend(loc="best")
        plt.ylabel("population, mln")
        plt.xticks(self.years, rotation=90)

        # plt.show()
        return sorted_regions

    @print_return
    def plot_growth(self):
        ''' plot bars for the 10 ten biggest populations'''
        if DEBUG:
            print("plot growth for top 10")

        ### using comprehension on two lists??? Can improve this?
        country_name = [self.countries[i, 0] for i in self.largest_indices]
        country_pop = [self.population[i, -1] for i in self.largest_indices]

        plt.bar(country_name, country_pop, edgecolor='blue') ### fix y and x ticks
        plt.title("Top 10 in 2019")
        plt.ylabel("population, mln")
        plt.xticks(country_name, rotation=45)

        # plt.show()
        return country_name


'''
#test drive
c = Population()
c.plot_trendCountries([6, 14, 100, 66, 34])
c.plot_growth()
c.plot_regionTrend()'''
