from .CsvTransformer import CsvTransformer

class FinancialDataTransformer(CsvTransformer):

    def __init__(self, logger, configs):
        super().__init__(logger, configs)
        self.type = None
        self.hasHeaders = False
        self.outputColumns = self.configs.get("OUTPUT_COLUMNS")
        self.inputColumns = []

    def setHasHeaders(self, hasHeaders):
        self.logger.debug("FinancialDataTransformer.setHasHeaders() " + str(hasHeaders))
        self.hasHeaders = hasHeaders

    def setType(self, type):
        self.logger.debug("FinancialDataTransformer.setType() " + type)
        self.type = type
        self.inputColumns = self.configs.get(self.type + "_COLUMNS")
    
    def removeHeader(self, data):
        self.logger.debug("FinancialDataTransformer.removeHeader()")
        if self.hasHeaders:
            data = data[1:]
        return data
    
    def applyHeader(self, array):
        array.append(self.outputColumns)
        return array
    
    def buildColumnMapValue(self, columnName):
        try:
            # Try to use another "interchangeable" column instead
            interchangeableColumns = self.configs.get("INTERCHANGEABLE_COLUMNS")
            isInterchangeableColumn = columnName in list(interchangeableColumns.keys())

            if isInterchangeableColumn:
                isInputColumn = interchangeableColumns[columnName] in self.inputColumns
                if isInputColumn:
                    interchangeableColumn = interchangeableColumns[columnName]
                    for index, name in enumerate(self.inputColumns):
                        if name == interchangeableColumn:
                            return index

            # Next, check out hard coded transformations
            if columnName is "SOURCE":
                return self.type

            # default
            return "DEFAULT"
        except Exception as e:
            self.logger.error("FinancialDataTransformer.buildColumnMapValue() Error", e)
            return "DEFAULT"
    
    # Retreives and organizes the order of columns using a pre-built map
    def applyColumnMap(self, columnMap, data):
        try:

            transformedData = []

            for row in data:
                transformedRow = []

                for valueOrIndex in columnMap:
                    if type(valueOrIndex) == str:
                        transformedRow.append(valueOrIndex)
                    else:
                        outputColumnValue = row[valueOrIndex]
                        transformedRow.append(outputColumnValue)
                    
                transformedData.append(transformedRow)
            
            return transformedData
        except Exception as e:
            self.logger.error("FinancialDataTransformer.applyTransformationMap() Error", e)
            return data

    # builds a map instructing how to reorder columns
    def getColumnMap(self):
        transformationMap = []

        for outputColumn in self.outputColumns:
            existsInInputColumns = outputColumn in self.inputColumns
            
            # If columns exists in input then use that column
            if existsInInputColumns:
                for index in range(len(self.inputColumns)):
                    if self.inputColumns[index] == outputColumn:
                        transformationMap.append(index)
                        break
            
            # Otherwise build the column value
            else:
                columnMapValue = self.buildColumnMapValue(outputColumn)
                transformationMap.append(columnMapValue)
            
        return transformationMap
    
    #Transform single value
    def transformValue(self, value):
        charactersToRemove = self.configs.get("CHARACTERS_TO_REMOVE")

        for character in charactersToRemove:
            value = value.replace(character, "")
        
        return value
            
    # Transform data into desired format
    def transform(self, data):
        try:
            self.logger.debug("FinancialDataTransformer.transform()")
            
            charactersToRemove = self.configs.get("CHARACTERS_TO_REMOVE")

            for rowIndex in range(len(data)):
                row = data[rowIndex]
                for columnIndex in range(len(row)):
                    column = row[columnIndex]
                    newColumn = self.transformValue(column)
                    row[columnIndex] = newColumn

            return data
        except Exception as e:
            self.logger.error("FinancialDataTransformer.transform() Error", e)
            return data
    
    # Transform data into standard set of columns ("OUTPUT_COLUMNS")
    def standardize(self, data):
        try:
            self.logger.debug("FinancialDataTransformer.standardize()")

            columnMap = self.getColumnMap()

            standardizedData = self.applyColumnMap(columnMap, data)

            return standardizedData
        except Exception as e:
            self.logger.error("FinancialDataTransformer.transform() Error", e)
            return data