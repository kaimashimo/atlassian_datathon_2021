import sys
from monte.dataHandler import *
from monte.engine import carlo

import os
from pathlib import Path
test_data_dir = Path(__file__).parent / "resources"
os.chdir(test_data_dir)

def arg_parse(args):
    """
    Given a list of command line arguments make sure that:
    a) qualification model file path is provided
    b) teamValue data set is given
    """
    if len(args) != 3:
        raise Exception("Usage: monte [qm Path] [tvDf Path]")

def main():
    """
    Args (respective order):
    - Qualification model path
    - Team model dataframe
    """

    # Make sure correct args are passed
    arg_parse(sys.argv)

    # Get team value data
    df = loadData(sys.argv[1])

    # Get qualification model dict
    qm = loadQualificationsModel(sys.argv[2])

    # Instantiate data class 
    bigCarlo = carlo(df, qm)

    # Run sim
    bigCarlo.runSim()

    # Write qualified to txt file
    writeToFile("results.txt", bigCarlo.qualified)