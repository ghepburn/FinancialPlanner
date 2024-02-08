from .BaseFinancialFileIdentifier import BaseFinancialFileIdentifier

class CsvFinancialFileIdentifer(BaseFinancialFileIdentifier):
    def getFileType(self, file):
        self.logger.debug("CsvFinancialFileIdentifier.getFileType()")
        if self.isBmoSharedChequingsFile(file):
            return self.configs.get("BMO_SHARED_CHEQUINGS_FILE_TYPE")
        
        if self.isBmoGregChequingsFile(file):
            return self.configs.get("BMO_GREG_CHEQUINGS_FILE_TYPE")
        
        if self.isBmoGregCreditCard(file):
            return self.configs.get("BMO_GREG_CREDIT_CARD_FILE_TYPE")
        
        self.logger.info("CsvFinancialFileIdentifier.getFileType() No file type could be identified.")

        return None