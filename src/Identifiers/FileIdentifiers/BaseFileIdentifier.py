

class BaseFileIdentifier:

    def __init__(self, logger, configs, columnIdentifier):
        self.logger = logger
        self.configs = configs
        self.columnIdentifier = columnIdentifier

    def isFileType(self, fileType):
        return False
        
    def getFileType(self, file):
        try: 
            self.logger.debug("BaseFileIdentifier.getFileType()")
            fileType = None

            supportedFileTypes = self.configs.get("SUPPORTED_FILE_TYPES")

            for supportedFileType in supportedFileTypes:
                isFileType = self.isFileType(file, supportedFileType)
                if isFileType:
                    fileType = supportedFileType
                    break
            
            if fileType is None:
                self.logger.info("BaseFileIdentifier.getFileType() No file type could be identified.")
            else:
                self.logger.debug("BaseFileIdentifier.getFileType() type is " + fileType)

            return fileType
        except Exception as e:
            self.logger.error("BaseFileIdentigier.getFileType() Error", e)

    def fileHasHeaders(self, file, fileType):
        try:
            fileColumns = self.configs.get(fileType + "_COLUMNS")
            firstRow = file[0]

            for index, item in enumerate(firstRow):
                columnName = fileColumns[index]
                isColumn = self.columnIdentifier.isColumn(columnName, item)
                if not isColumn:
                    return True
            
            return False
        except Exception as e:
            self.logger.error("BaseFileIdentifier.fileHasHeaders() Error", e)
            return False
    