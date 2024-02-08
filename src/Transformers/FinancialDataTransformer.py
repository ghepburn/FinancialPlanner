from .CsvTransformer import CsvTransformer

class FinanceDataTransformer(CsvTransformer):

    def __init__(self, logger, configs):
        CsvTransformer().__init__(logger, configs)
        self.type = None

    def setType(self, type):
        self.type = type

    def getTypeMap(self, type):
        pass
    
    def transform(self, csv):
        data = self.csvToObject(csv)
        print(data[0])
        
        self.getTypeMap(self.type)
        
        return data