from sklearn.preprocessing import StandardScaler
import math

class carlo:
    """
    Carlo is a class that stores important stuff
    """
    def __init__(self, tvDF, qmDict):
        self.teamValueDF = tvDF
        self.qualModelDict = qmDict

def valuetoProba(teamValueDF):
    """
    Given a team value df:
    1. Normalise values
    2. apply logistic sigmoid to get a proba
    """
    scaler = StandardScaler()
    teamValueDF.value = scaler.fit_transform(teamValueDF.value.to_numpy().reshape(-1, 1))
    teamValueDF.value = teamValueDF.value.transform(lambda x: 1 / (1 + math.exp(-x)))
    return teamValueDF

    

