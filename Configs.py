

import json

class Configs:
    values = {
        "LOCAL_DATA_DIRECTORY": "./data",
        "GOOGLE_DRIVE_DIRECTORY_PATH": [],
        "DESIRED_GOOGLE_DRIVE_DOWNLOADED_FILE_TYPE": "text/csv",
        "TEST_GOOGLE_DRIVE_FILE_ID": "",
        
        # Financial File Types
        "FINANCIAL_FILE_TYPES": [
            "BMO_CHEQUINGS_FILE_TYPE", 
            "BMO_CREDIT_CARD_FILE_TYPE"
        ],

        # Column Mapping
        
        
    }
    
    def __init__(self, logger):
        self.logger = logger
        self.loadSecrets()

    def loadSecrets(self):
        self.logger.debug("Configs.loadSecrets()")
        
        f = open("secrets.json", "r")
        jsonSecrets = f.read()
        secrets = json.loads(jsonSecrets)
        
        for key in secrets.keys():
            self.values[key] = secrets[key]

        self.logger.debug("Configs.loadSecrets() Secrets Set")
        
    def get(self, name):
        try:
            return self.values[name]
        except Exception as e:
            self.logger.error("Error name config does not exist. ", e)