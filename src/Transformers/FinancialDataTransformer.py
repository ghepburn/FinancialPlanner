from .CsvTransformer import CsvTransformer

class FinancialDataTransformer(CsvTransformer):

    def __init__(self, logger, configs):
        super().__init__(logger, configs)
        self.type = None

    def setType(self, type):
        self.type = type

    def getTypeMap(self, type):
        pass
    
    def transform(self, data):
        self.logger.debug("FinancialDataTransformer.transform()")
        
        self.getTypeMap(self.type)
        
        return data