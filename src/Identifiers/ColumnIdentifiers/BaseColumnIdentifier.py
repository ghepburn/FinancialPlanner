

class BaseColumnIdentifier:
    def __init__(self, logger, configs):
        self.logger = logger
        self.configs = configs
        self.allColumnDetails = self.configs.get("COLUMN_DETAILS")

    def isType(self, columnType, data):
        return columnType == type(data)
    
    def isLength(self, columnLength, data):
        if type(columnLength) == int:
            isCorrectLength = (len(data) == columnLength)
        else:
            minLength = columnLength[0]
            maxLength = columnLength[-1]

            isMinimumLength = (len(data) >= minLength)
            isNotOverMaximumLength = (len(data) <= maxLength)
            isCorrectLength = (isMinimumLength and isNotOverMaximumLength)

        return isCorrectLength

    def isColumn(self, columnName, data):
        try:
            columnDetails = self.allColumnDetails[columnName]

            isCorrectType = self.isType(columnDetails["type"], data)
            if not isCorrectType:
                self.logger.debug("BaseColumnIdentifier.isColumn() " + columnName + " is type " + str(type(data)) + " but we were expecting type " + str(columnDetails["type"]))
                return False
            
            isCorrectLength =self.isLength(columnDetails["length"], data)
            if not isCorrectLength:
                self.logger.debug("BaseColumnIdentifier.isColumn() " + columnName + " length (" + str(len(data)) + ") is invalid")
                return False
            
            return True
        except Exception as e:
            self.logger.error("BaseColumnIdentifier.isColumn() Error", e)
            return False