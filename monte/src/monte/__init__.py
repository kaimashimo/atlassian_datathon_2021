import sys
from monte.dataHandler import *
from monte.engine import carlo

def arg_parse(args):
    """
    Given a list of command line arguments make sure that:
    a) qualification model file path is provided
    b) teamValue data set is given
    """
    if len(args) != 2:
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
    df = loadData(sys.argv[0])

    # Get qualification model dict
    qm = loadQualificationsModel(sys.argv[1])

    # Instantiate data class 
    bigCarlo = carlo(df, qm)

