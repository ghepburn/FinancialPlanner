from .CsvTransformer import CsvTransformer

class FinancialDataTransformer(CsvTransformer):

    def __init__(self, logger, configs):
        super().__init__(logger, configs)
        self.type = None
        self.hasHeaders = False
        self.outputColumns = self.configs.get("OUTPUT_COLUMNS")
        self.inputColumns = []

    def setHasHeaders(self, hasHeaders):
        self.hasHeaders = hasHeaders

    def setType(self, type):
        self.type = type
        self.inputColumns = self.configs.get(self.type + "_COLUMNS")
    
    def removeHeaders(self, data):
        if self.hasHeaders:
            data = data[1:]
        return data
    
    def applyHeader(self, data):
        return [self.outputColumns] + data
    
    def buildColumnMapValue(self, columnName):
        try:
            self.logger.debug("FinancialDataTransformer.buildColumnMapValue() " + columnName)

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
    
    # Transform data using a map
    # maps built from self.getTransformationMap
    # string values are applied to every row
    # otherwise, the value is an index and we grab an existing column
    def applyTransformationMap(self, transformationMap, data):
        try:

            transformedData = []

            for row in data:
                transformedRow = []

                for valueOrIndex in transformationMap:
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

    
    def getTransformationMap(self, data):
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
            
    # Transform data into desired format
        # Step #1 Define columns
        # Step #2 Correct formatting in each column
    def transform(self, data):
        try:
            self.logger.debug("FinancialDataTransformer.transform()")

            data = self.removeHeaders(data)

            transfomrationMap = self.getTransformationMap(data)

            transformedData = self.applyTransformationMap(transfomrationMap, data)

            transformedDataWithHeader = self.applyHeader(transformedData)

            self.logger.debug(transformedDataWithHeader)

            return transformedDataWithHeader
        except Exception as e:
            self.logger.error("FinancialDataTransformer.transform() Error", e)
            return data