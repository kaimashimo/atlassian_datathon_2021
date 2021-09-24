import pandas as pd
import json
import argparse

def argParse(args):
    """
    Given a list of command line arguments make sure that:
    a) qualification model file path is provided
    b) teamValue data set is given
    """
    parser = argparse.ArgumentParser(description="monte simulates FIFA matches to precit which teams will qualify for the FIFA world cup using Monte Carlo methods")
    parser.add_argument("tvDF", metavar="tvDF", type=str, help="path to the team value dataframe")
    parser.add_argument("qmJSON", metavar="qmJSON", type=str, help="path to the qualification model JSON")
    parser.add_argument("bt", nargs="?", metavar="bt", type=str, help="[OPTIONAL] path to backtesting results for validation")
    args = parser.parse_args()
    
    if ".csv" not in args.tvDF:
        raise argparse.ArgumentTypeError("Team value df must be a csv file")
    if ".json" not in args.qmJSON:
        raise argparse.ArgumentTypeError("Qualification model must be a json file")
    if args.bt is not None and ".txt" not in args.bt:
        raise argparse.ArgumentTypeError("Backtest results must be a text file")

    return args

def loadData(path):
    """Function takes a path (string) and returns a pandas dataframe"""
    try:
        return pd.read_csv(path)
    except Exception as e:
        raise Exception("Could not read df, possbily incorrect path: {}".format(e))

def loadQualificationsModel(path):
    """Takes qualification model JSON file and returns usable dict"""
    try:
        f = open(path)
    except Exception as e:
        raise Exception("Could not read df, possbily incorrect path: {}".format(e))

    data = json.load(f)

    f.close()

    return data

def writeToFile(path, lst):
    with open(path,'w') as f:
        for item in lst:
            f.write("{}\n".format(item))
