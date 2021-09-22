from numpy.lib.twodim_base import diag
from sklearn.preprocessing import StandardScaler
import random
import math
import numpy as np 
import pandas as pd
import itertools

class carlo:
    """
    Carlo is a class that stores important stuff
    """
    def __init__(self, tvDF, qmDict):
        self.teamValueDF = _valuetoProba(tvDF)
        self.qualModelDict = qmDict

        # List of regions
        self.regions = list(filter(lambda x: x != "playoffs", self.qualModelDict.keys()))      

        # List of team names who have qualified (gets filled later)
        self.qualified = []

        # Dict of win counts for each country in each region (df gets filled in later)
        self.regionalTables = {region:pd.DataFrame([], columns = ["country", "points"]) for region in self.qualModelDict.keys()}
        
        # dict of all possible team matchings within regions
        self.regionalCombinations = self._combinationsPerRegion()

    def _combinationsPerRegion(self):
        """Create pairings for all possible teams per region and return list of tuples of combinations"""
        regionalCombinations = {region: [] for region in self.qualModelDict.keys()}
        for region in self.regions:
            combinations = _generateCombinations(self.teamValueDF.loc[self.teamValueDF.region == region].country)
            regionalCombinations[region] = combinations
        return regionalCombinations

    def _insertIntoRegionalTables(self, regionStr, countriesList):
        """
        Insert all countries from a given list of country strings into their respective regional table.
        Returns None.
        """

        df = self.regionalTables[regionStr]
        for country in countriesList: df = df.append({"country":country, "points":0}, ignore_index=True)
        self.regionalTables[regionStr] = df

    def _incrementScore(self, regionStr, countryStr):
        """
        Given a region and a country, increment countries score in their respective regional table
        """
        df = self.regionalTables[regionStr]
        df.at[df.loc[df.country == countryStr].index.item(), "points"] += 1
        self.regionalTables[regionStr] = df

    def _playGamePerRegion(self, regions, combinationsDict):
        """
        For a given region (e.g. UEFA or playoffs) play game and populate regional tables.
        No return value, all transforms are internal.
        """
        for region in regions:
            # Insert all countries from region into regional table (each country start at 0)
            self._insertIntoRegionalTables(region, self.teamValueDF.loc[self.teamValueDF.region == region].country.to_list())
            pairs = combinationsDict[region]
            # Play games for each pair, default n = 10,000
            for pair in pairs:
                team1Proba = self.teamValueDF.loc[self.teamValueDF.country == pair[0]].value.item()
                team2Proba = self.teamValueDF.loc[self.teamValueDF.country == pair[1]].value.item()
                team1Won = _playGame(team1Proba, team2Proba)
                # If team 1 won increment their score, otherwise team 2's
                if team1Won: self._incrementScore(region, pair[0])
                else: self._incrementScore(region, pair[1])
    
"""
1. Within each region run every combination of match and create table (1st, 2nd, 3rd, etc.)
2. According to qual model teams in each region either get assigned to 
    a) passed i.e. gets into fifa
    b) goes to play-offs
3. should probably create another function that will run the whole sim
"""

def _generateCombinations(countries):
    """Given a list of countries from a region return a list of all possible combinations"""
    return list(itertools.combinations(countries, 2))


def _playGame(team1Proba, team2Proba, n = 10000):
    """
    Given a pair of countrie's probabiltiies flip coin N times and return the winner
    Return true if team1 wins (never assume draw)
    """
    team1 = [__flip(team1Proba) for _ in range(n)]
    team2 = [__flip(team2Proba) for _ in range(n)]
    return (np.sum(team1) >= np.sum(team2))
        
def __flip(p):
    """
    Flip coin once, from uniform distribution, return 1 if heads, else 0.
    Accepts probability p and is only heads if distribution pulls a probability at least as rare as p.
    """
    return 1 if random.random() < p else 0

def _valuetoProba(teamValueDF):
    """
    Given a team value df:
    1. Normalise values
    2. apply logistic sigmoid to get a proba
    """
    scaler = StandardScaler()
    teamValueDF.value = scaler.fit_transform(teamValueDF.value.to_numpy().reshape(-1, 1))
    teamValueDF.value = teamValueDF.value.transform(lambda x: 1 / (1 + math.exp(-x)))
    return teamValueDF

    

