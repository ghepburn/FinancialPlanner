from .BaseFileIdentifier import BaseFileIdentifier

class FinancialFileIdentifier(BaseFileIdentifier):
    def isFileType(self, fileData, fileType):
        self.logger.debug("CsvFinancialFileIdentifier.isFileType() " + fileType)

        try:
            fileColumns = self.configs.get(fileType + "_COLUMNS")
            allColumnDetails = self.configs.get("COLUMN_DETAILS")

            row = fileData[1]
                
            isCorrectLength = (len(row) == len(fileColumns))
            if not isCorrectLength:
                self.logger.debug("CsvFinancialFileIdentifer.isFileType() row length is " + str(len(row)) + " but we were expecting length " + str(len(fileColumns)))
                return False
            
            for index in range(len(fileColumns)):
                columnName = fileColumns[index]
                columnDetails = allColumnDetails[columnName]
            
                isSameDataType = (type(row[index]) == columnDetails["type"])
                if not isSameDataType:
                    self.logger.debug("CsvFinancialFileIdentifer.isFileType() " + columnName + " is type " + str(type(row[index])) + " but we were expecting type " + str(columnDetails["type"]))
                    return False
                
                if type(columnDetails["length"]) == int:
                    isSameLength = (len(row[index]) == columnDetails["length"])
                else:
                    isMinimumLength = (len(row[index]) > columnDetails["length"][0])
                    isNotMaximumLength = (len(row[index]) < columnDetails["length"][-1])
                    isSameLength = (isMinimumLength and isNotMaximumLength)
                if not isSameLength:
                    self.logger.debug("CsvFinancialFileIdentifer.isFileType() " + columnName + " length (" + str(len(row[index])) + ") is invalid")
                    return False
                
            return True
                
                


        except Exception as e:
            self.logger.error("CsvFinancialFileIdentifier.isFileType() Error while called with type " + fileType, e)
            return False