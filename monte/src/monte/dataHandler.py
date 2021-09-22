import pandas as pd
import json

def loadData(path):
    """Function takes a path (string) and returns a pandas dataframe"""
    try:
        return pd.read_csv(path)
    except Exception as e:
        raise Exception("Could not read df, possbily incorrect path: {}".format(e))

def loadQualificationsModel(path):
    """Takes qualification model JSON file and returns usable dict"""
    try:
        f = open(path, )
    except Exception as e:
        raise Exception("Could not read df, possbily incorrect path: {}".format(e))

    data = json.load(f)

    f.close()

    return data
