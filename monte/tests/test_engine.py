# Ensure working in current dir
import os
from pathlib import Path
test_data_dir = Path(__file__).parent / "resources"
os.chdir(test_data_dir)

from monte.engine import *
from monte.dataHandler import loadData

def test_valueToProba():
    df = loadData("teamValueTest.csv")
    transformedDf = valuetoProba(df)
    print(transformedDf)
