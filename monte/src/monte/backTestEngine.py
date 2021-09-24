class backtest:
    def __init__(self, simResults, btPath):
        self.actual = self.loadBackTestResults(btPath)
        self.simReults = simResults
        self.correctPredsList = self.correctPreds()

    def loadBackTestResults(self, path):
        """Given a file path, load backtest results (expects .txt)"""
        try:
            f = open(path, "r")
        except Exception as e:
            raise Exception("Could not read test file, possbily incorrect path: {}".format(e))
        return [x.replace("\n", "") for x in f.readlines()]

    def accuracy(self):
        """Calulcates accuracy by comparing simulation results with actual results"""
        return len(self.correctPredsList) / len(self.simReults)
    
    def correctPreds(self):
        actual = Lower(self.actual)
        preds = Lower(self.simReults)
        return set(actual) & set(preds)

    def numCorrectPreds(self):
        return len(self.correctPredsList)
    
    def numFalsePreds(self):
        return len(self.actual) - len(self.correctPredsList)

    def printResults(self):
        acc = self.accuracy()
        numCorrectPreds = self.numCorrectPreds()
        numFalsePreds = self.numFalsePreds()
        print("Accuracy of backtest: {:.2f}".format(acc))
        print("{} correct preds".format(numCorrectPreds))
        print("{} incorrect preds".format(numFalsePreds))
        print("List of correctly predicted countries: {}".format(self.correctPredsList))

def Lower(lst):
    """Utility function to convert a list of strings to lower case"""
    return [x.lower() for x in lst]