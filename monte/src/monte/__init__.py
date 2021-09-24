import sys
from monte.backTestEngine import backtest
from monte.dataHandler import *
from monte.simulationEngine import carlo

import os
from pathlib import Path
data_dir = Path(__file__).parent / "resources"
os.chdir(data_dir)

def main():
    """
    Args (respective order):
    - Qualification model path
    - Team model dataframe
    """

    # Make sure correct args are passed
    args = argParse(sys.argv)
    print(args)

    # Get team value data
    df = loadData(args.tvDF)

    # Get qualification model dict
    qm = loadQualificationsModel(args.qmJSON)

    # Instantiate data class 
    bigCarlo = carlo(df, qm)

    # Run sim
    bigCarlo.runSim()

    # Write qualified to txt file
    writeToFile("results_{}.txt".format(args.tvDF.replace(".csv", "")), bigCarlo.qualified)

    # validate results with backtest data (optional)
    if args.bt is not None: backtest(bigCarlo.qualified, args.bt).printResults()
                 