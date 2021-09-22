# Ensure working in current dir
import os
from pathlib import Path
test_data_dir = Path(__file__).parent / "resources"
os.chdir(test_data_dir)

from monte.engine import carlo, _playGame, _valuetoProba 
from monte.dataHandler import loadData, loadQualificationsModel

def test_carlo():
    bigBoi = carlo(loadData("teamValueTest2.csv"), loadQualificationsModel("qualificationModel.json"))
    print(bigBoi.teamValueDF, bigBoi.qualModelDict, bigBoi.regionalTables, bigBoi.regionalCombinations, bigBoi.regions)

    # Ensure that class variables have been initialised correctly
    assert(len(bigBoi.regionalTables) == 7)
    assert(len(bigBoi.regionalCombinations) == 7)
    assert(len(bigBoi.regions) == 6)

def test_insertIntoRegionalTables():
    bigBoi = carlo(loadData("teamValueTest2.csv"), loadQualificationsModel("qualificationModel.json"))

    # Insert new values
    bigBoi._insertIntoRegionalTables("AFC", ["Australia", "South Korea"])
    bigBoi._insertIntoRegionalTables("UEFA", ["France"])
    print(bigBoi.regionalTables)
    assert(bigBoi.regionalTables["AFC"].shape[0] == 2) # 2 cols
    assert(bigBoi.regionalTables["UEFA"].shape[0] == 1) # 1 col

    # Increment current countries
    bigBoi._incrementScore("AFC", "Australia")
    bigBoi._incrementScore("AFC", "Australia")
    bigBoi._incrementScore("UEFA", "France")
    print(bigBoi.regionalTables)
    assert(bigBoi.regionalTables["AFC"].points.sum() == 2) # Aus: 2, SK: 0
    assert(bigBoi.regionalTables["UEFA"].points.sum() == 1) # France: 1

def test_playGamePerRegion():
    bigBoi = carlo(loadData("teamValueTest2.csv"), loadQualificationsModel("qualificationModel.json"))
    bigBoi._playGamePerRegion(bigBoi.regions, bigBoi.regionalCombinations)
    print(bigBoi.regionalTables)
    regionsToCheck = ["UEFA", "CONMEBOL", "CONCACAF", "CAF", "AFC"]
    for region in regionsToCheck: assert(not bigBoi.regionalTables[region].empty)

def test_valueToProba():
    df = loadData("teamValueTest.csv")
    transformedDf = _valuetoProba(df)
    print(transformedDf)

def test_playGame():
    print(_playGame(0.9, 0.6))