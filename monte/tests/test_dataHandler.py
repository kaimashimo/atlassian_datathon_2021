import pytest
from monte.dataHandler import *

# Ensure working in current dir
import os
from pathlib import Path
test_data_dir = Path(__file__).parent / "resources"
os.chdir(test_data_dir)

def test_argParse():
    # Ensure raises error if incorrect file type
    try: 
        argParse(["py", "test", "test"])
        pytest.raises(Exception("Should raise error cause incorrect args"))
    except SystemExit:
        pass
    
    # Test backtest results arg parse
    try: 
        argParse(["py", "test.csv", "test.json", "bt"])
        pytest.raises(Exception("Should raise error cause incorrect args"))
    except SystemExit:
        pass


def test_loadData():
    df = loadData("teamValueTest.csv")
    print(df)

    # Columns should be 2
    assert(df.shape[0] == 3)
    # Rows should be 3
    assert(df.shape[1] == 3)

def test_loadQualModel():
    qm = loadQualificationsModel("qualificationModel.json")
    print(qm)
    assert(len(qm) == 6)

def test_writeToFile():
    writeToFile('results.txt', ["Australia", "Argentina"])
