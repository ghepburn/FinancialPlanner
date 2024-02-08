from .GoogleDriveClient import GoogleDriveClient

class GoogleDriveManager:
    def __init__(self, logger, configs):
        self.logger = logger
        self.configs = configs

        self.client = GoogleDriveClient(logger, configs)

    def isFile(self, googleDriveItem):
        self.logger.debug("GoogleDriveManager.isFile()")
        self.logger.debug(googleDriveItem)
        if (googleDriveItem["mimeType"][-6:] != "folder"):
            return True
        return False

    def getChildFolderFromFolderPath(self, folderPath):
        try:
            self.logger.debug("GoogleDriveManager.getChildFolderFromFolderPath()")
            parentFolderId = None
            for folderName in folderPath:
                if not parentFolderId:
                    parentFolders = self.client.get(folderName)
                    if not parentFolders:
                        self.logger.error(folderName + " folder not retrieved from Google Drive Api.")
                        return
                    
                    parentFolder = parentFolders[0]
                    parentFolderId = parentFolder["id"]

                else:
                    parentChildren = self.client.getFolderChildren(parentFolderId)
                    if not parentChildren:
                        self.logger.error("Folder children not retrieved from Google Drive Api.")
                        return
                    
                    for child in parentChildren:
                        if child["name"] == folderName:
                            parentFolderId = child["id"]

            return parentFolderId
        except Exception as e:
            self.logger.error("GoogleDriveManager.getChildFolderFromFolderPath()", e)
            return

    def getAllLowerFileIds(self, folderId, fileIds = []):
        self.logger.debug("GoogleDriveManager.getAllLowerFileIds()")

        children = self.client.getFolderChildren(folderId)
        for child in children:
            if self.isFile(child):
                fileIds.append(child["id"])
            else:
                fileIds = self.getAllLowerFileIds(child["id"], fileIds)

        return fileIds

    def get(self, fileId):
        self.logger.debug("GoogleDriveManager.get() " + fileId)
        fileType = self.configs.get("DESIRED_GOOGLE_DRIVE_DOWNLOADED_FILE_TYPE")
        downloadedBytes = self.client.download(fileId, fileType)
        return downloadedBytes