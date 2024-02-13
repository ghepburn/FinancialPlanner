import os
import pandas as pd

from src.GoogleDrive.GoogleDriveManager import GoogleDriveManager
from src.Identifiers import FinancialFileIdentifier
from src.Identifiers import FinancialColumnIdentifier
from src.Transformers import FinancialDataTransformer

class DataManager:

    def __init__(self, logger, configs):
        self.logger = logger
        self.configs = configs
        
        self.data_directory = configs.get("LOCAL_DATA_DIRECTORY")
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
            return data
        except Exception as e:
            self.logger.error("DataManager.save() Failed.", e)

    def downloadData(self):
        self.logger.debug("DataManager.downloadData()")
        try:

            # Identify Files Ids
            # folderId = self.googleDriveManager.getChildFolderFromFolderPath(self.google_drive_directory_path)
            # fileIds = self.googleDriveManager.getAllLowerFileIds(folderId)
            # self.logger.debug("DataManager.downloadData() Retrieved " + str(len(fileIds)) + " fileIds")
            fileIds = [self.configs.get("TEST_GOOGLE_DRIVE_FILE_ID")]

            # Get Data
            data = []
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
                transformedData = self.transformer.transform(data)

                data.append(transformedData)

            # Combine Data
            data = self.combineData(transformedData)

            # Save Data
            self.save(data)

            self.logger.info("DataManager.download() Downloaded Data Successfully.")

            return data
            
        except Exception as e:
            self.logger.error("Error during dataManager.downloadData()", e)
    
    