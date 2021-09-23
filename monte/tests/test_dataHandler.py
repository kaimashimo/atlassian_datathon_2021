# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

from monte.dataHandler import loadData, loadQualificationsModel, writeToFile

# Ensure working in current dir
import os
from pathlib import Path
test_data_dir = Path(__file__).parent / "resources"
os.chdir(test_data_dir)

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
    writeToFile('results.txt')

