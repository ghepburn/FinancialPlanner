from .BaseFileIdentifier import BaseFileIdentifier

class FinancialFileIdentifier(BaseFileIdentifier):
    def isFileType(self, fileData, fileType):
        self.logger.debug("FinancialFileIdentifier.isFileType() " + fileType)

        try:
            fileColumns = self.configs.get(fileType + "_COLUMNS")

            row = fileData[1]
                
            isCorrectLength = (len(row) == len(fileColumns))
            if not isCorrectLength:
                self.logger.debug("FinancialFileIdentifier.isFileType() row length is " + str(len(row)) + " but we were expecting length " + str(len(fileColumns)))
                return False
            
            for index in range(len(fileColumns)):
                columnName = fileColumns[index]

                isColumn = self.columnIdentifier.isColumn(columnName, row[index])
                if not isColumn:
                    self.logger.debug("FinancialFileIdentifier.isFileType() " + columnName + " is not " + fileColumns[index])
                    return False
                
            return True
                
                


        except Exception as e:
            self.logger.error("FinancialFileIdentifier.isFileType() Error while called with type " + fileType, e)
            return False