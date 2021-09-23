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
    
    def _printRegionalTables(self):
        for region in self.regionalTables.keys():
            print(region + ":")
            print(self.regionalTables[region].sort_values("points", ascending=False).reset_index(drop=True))
            print()
    
    def runSim(self):
        """
        Driver program runs monte carlo simultion.
        First run games per region then based off qualification model, choose which teams go to international playoffs.
        Returns None.
        """
        print("Play games per region...")
        # Play game per region to populate team score tables per region
        self._playGamePerRegion(self.regions, self.regionalCombinations)
        print("Done")
        self._printRegionalTables()

        # Decide which teams go to playoffs and which have qualified
        for region in self.regions:
            # Top n teams qualify directly
            n = self.qualModelDict[region]["direct"]
            # in qm dict playoffs is defined as nTh team goes to playoffs, but df is indexed starting from 0
            nPlayoffs = self.qualModelDict[region]["playoffs"] - 1 

            # Select top N teams that go directly to the FIFA
            regionTable = self.regionalTables[region].sort_values("points", ascending=False).reset_index(drop=True)
            topNTeams = regionTable.head(n).country.to_list()
            self.qualified += topNTeams

            # Check which countries must go to international playoffs
            if nPlayoffs >= 0:
                country = regionTable.iloc[nPlayoffs].country

                # Change country region to playoffs 
                self.teamValueDF.at[self.teamValueDF.loc[self.teamValueDF.country == country].index.item(), "region"] = "playoffs"

        # Run admin operations to ensure playoffs run smoothly
        playOffCountries = self.teamValueDF.loc[self.teamValueDF.region == "playoffs"].country.to_list()
        self.regionalTables = {"playoffs":pd.DataFrame([], columns = ["country", "points"])}
        playOffsCombinations = {"playoffs":_generateCombinations(playOffCountries)}

        # Run playoffs & select winners that qualify
        print("Running playoffs...")
        self._playGamePerRegion(["playoffs"], playOffsCombinations)
        print("Done")
        self._printRegionalTables()
        n = self.qualModelDict["playoffs"]["direct"]
        regionTable = self.regionalTables["playoffs"].sort_values("points", ascending=False).reset_index(drop=True)
        topNTeams = regionTable.head(n).country.to_list()
        self.qualified += topNTeams


        """
        For each region:
            sort table dict then:
                select top N teams that go directly to the FIFA
                If region supports playoffs (i.e. not -1) then:
                    select team on the ladder that goes to playoffs and,
                    change their region to playoffs in team value df
        Select all countries that go to playoffs then,
        replace the regionalTables dict with {"playoffs": dataframe(country, points)} and,
        create new regionalCombinations list with all countries in playoffs

        Run: play game per region with new list of playoff countries and regional combinations list
        Once done sort dataframe and select top N teams that can qualify from regionals

        Algorithm is done, self.qualified should be full with all teams
        __init__ should write these teams to a text file
        """

def _topNteams(scoresDf, n):
    """Given a regional scores df, retrieve top N countries from dataframe"""
    sortedDf = scoresDf.sort_values("points", ascending=False).reset_index(drop=True)
    return sortedDf.head(n).country.to_list()

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

    

