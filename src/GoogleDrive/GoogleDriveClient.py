import os.path
import io

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

class GoogleDriveClient:
    def __init__(self, logger, configs):
        self.logger = logger

    def authenticate(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open("token.json", "w") as token:
                    token.write(creds.to_json())

        return creds

    def getService(self):
        creds = self.authenticate()
        service = build("drive", "v3", credentials=creds)
        return service

    # Retrieves files/folders from Google Drive API by name
    # 
    # Example Response: [{"kind": "drive#file", "mimeType": "application/vnd.google-apps.folder", "id": "1SZm6wHJbxuE_RC_uifpsB3ivjxBrS4ug", "name": "Finances"}]
    # 
    def get(self, name):
        self.logger.debug("GoogleDriveClient.get() " + name)
        try:
            service = self.getService()

            # Call the Drive v3 API
            query="name = '" + name + "'"
            results = service.files().list(q=query).execute()
            items = results.get("files", [])

            if not items:
                self.logger.info("GoogleDriveClient.get() item not found with query " + query)
                return
                
            else:
                self.logger.info("GoogleDriveClient.get() Found " + str(len(items)) + " items with query " + query)
                self.logger.info(items)

            return items
        except Exception as e:
            self.logger.error("Error during GoogleDriveClient.get()", e)
            return
    
    def getFolderChildren(self, folderId):
        self.logger.debug("GoogleDriveClient.getFolderChildren()")
        try:
            service = self.getService()

            # Call the Drive v3 API
            query="parents = '" + folderId + "'"
            results = service.files().list(q=query).execute()
            items = results.get("files", [])

            if not items:
                self.logger.info("GoogleDriveClient.getFolderChildren() item not found with query " + query)
            else:
                self.logger.info("GoogleDriveClient.getFolderChildren() Found " + str(len(items)) + " items with query " + query)

            return items
        except Exception as e:
            self.logger.error("Error during GoogleDriveClient.getFolderChildren()", e)
            return
    
    def download(self, id, type):
        self.logger.debug("GoogleDriveClient.download() " + type)
        service = self.getService()
        
        results = service.files().export_media(fileId=id, mimeType=type).execute()
        if results:
            self.logger.info("GoogleDriveClient.download() Downloaded " + type + " " + id)
        
        return results
