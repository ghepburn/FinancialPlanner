import os
import csv

from src.GoogleDrive.GoogleDriveManager import GoogleDriveManager
from src.Identifiers import FinancialFileIdentifier
from src.Identifiers import FinancialColumnIdentifier
from src.Transformers import FinancialDataTransformer

class DataManager:

    def __init__(self, logger, configs):
        self.logger = logger
        self.configs = configs
        
        self.data_directory = configs.get("LOCAL_DATA_DIRECTORY")
        self.fileName = self.configs.get("LOCAL_DATA_FILE_NAME")

        self.google_drive_directory_path = configs.get("GOOGLE_DRIVE_DIRECTORY_PATH")

        self.googleDriveManager = GoogleDriveManager(logger, configs)
        
        columnIdentifier = FinancialColumnIdentifier(logger, configs)
        self.identifier = FinancialFileIdentifier(logger, configs, columnIdentifier)
        self.transformer = FinancialDataTransformer(logger, configs)

    def deleteData(self):
        self.logger.debug("DataManager.deleteData()")
        try:
            if self.data_directory is not None:
                os.rmdir(self.data_directory)
                self.logger.info(self.data_directory + " was deleted.")
        except Exception as e: 
            self.logger.error("Error during dataManager.deleteData()", e)

    def createDirectory(self):
        self.logger.debug("DataManager.createDirectory()")
        try:
            if self.data_directory is not None:
                os.mkdir(self.data_directory)
                self.logger.info(self.data_directory + " has been created.")
        except Exception as e:
            self.logger.error("Error during dataManager.createDirectory()", e)

    def save(self, data):
        self.logger.debug("DataManager.save()")
        try:
            with open(self.data_directory + "/" + self.fileName, 'w') as file:
                writer = csv.writer(file)
                for row in data:
                    writer.writerow(row)
        except Exception as e:
            self.logger.error("DataManager.save() Error ", e)

    def combineData(self, data):
        self.logger.debug("DataManager.combineData()")

        combinedData = []

        combinedData = self.transformer.applyHeader(combinedData)
        
        for file in data:
            for row in file:
                combinedData.append(row)
        
        return combinedData

    def downloadData(self):
        self.logger.debug("DataManager.downloadData()")
        try:

            # Identify Files Ids
            useTestFile = self.configs.get("USE_TEST_FILE")
            if useTestFile:
                fileIds = [self.configs.get("TEST_GOOGLE_DRIVE_FILE_ID")]
            else:
                folderId = self.googleDriveManager.getChildFolderFromFolderPath(self.google_drive_directory_path)
                fileIds = self.googleDriveManager.getAllLowerFileIds(folderId)
                self.logger.debug("DataManager.downloadData() Retrieved " + str(len(fileIds)) + " fileIds")

            # Get Data
            csvFiles = []
            for id in fileIds:
                fileBytes = self.googleDriveManager.get(id)
                csv = fileBytes.decode()

                data = self.transformer.csvToObject(csv)

                # Identify Data Type
                fileType = self.identifier.getFileType(data)
                fileHasHeaders = self.identifier.fileHasHeaders(data, fileType)

                # Transform Data
                self.transformer.setType(fileType)
                self.transformer.setHasHeaders(fileHasHeaders)
                dataWithoutHeader = self.transformer.removeHeader(data)
                standardizedData = self.transformer.standardize(dataWithoutHeader)
                transformedData = self.transformer.transform(standardizedData)

                csvFiles.append(transformedData)

            # Combine Data
            data = self.combineData(csvFiles)

            # Save Data
            self.save(data)

            self.logger.info("DataManager.download() Downloaded Data Successfully.")

            return data
            
        except Exception as e:
            self.logger.error("Error during dataManager.downloadData()", e)

    def getData(self):
        dataExists = False
        useCache = self.configs.get("USE_CACHE")
        if useCache:
            directoryExists = os.path.isdir(self.data_directory)
            if directoryExists:
                dataExists = os.path.isfile(self.data_directory + "/" + self.fileName)

        if dataExists:
            pass
        else:
            self.deleteData()
            self.createDirectory()
            self.downloadData()
    
    