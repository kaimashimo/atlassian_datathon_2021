from monte.backTestEngine import backtest

# Ensure working in current dir
import os
from pathlib import Path
test_data_dir = Path(__file__).parent / "resources"
os.chdir(test_data_dir)

def test_loadBackTestResults():
    bt = backtest([], "2018FifaResultsTest.txt")
    assert(len(bt.actual) == 3)

def test_metrics():
    bt = backtest(["WRONG", "South Korea", "Japan"], "2018FifaResultsTest.txt")
    bt.printResults()
    assert(bt.accuracy() == 1)
    assert(bt.numCorrectPreds() == 2)
    assert(bt.numFalsePreds() == 1)

