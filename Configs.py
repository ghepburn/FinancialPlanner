

import json

class Configs:
    values = {
        "LOCAL_DATA_DIRECTORY": "./data",
        "GOOGLE_DRIVE_DIRECTORY_PATH": [],
        "DESIRED_GOOGLE_DRIVE_DOWNLOADED_FILE_TYPE": "text/csv",
        "TEST_GOOGLE_DRIVE_FILE_ID": "",
        
        "SUPPORTED_FILE_TYPES": [
            "BMO_CHEQUINGS_FILE", 
            "BMO_CREDIT_CARD_FILE"
        ],

        # File Column Mappings
        "BMO_CHEQUINGS_FILE_COLUMNS": ["CARD_NUMBER", "TRANSACTION_TYPE", "POST_DATE", "TRANSACTION_AMOUNT", "DESCRIPTION"],
        "BMO_CREDIT_CARD_FILE_COLUMNS": ["ITEM_NUMBER", "CARD_NUMBER", "TRANSACTION_DATE", "TRANSACTION_MONTH", "POST_DATE", "TRANSACTION_AMOUNT", "DESCRIPTION"],

        # Column Details
        "COLUMN_DETAILS": {
            "CARD_NUMBER": {"type": str, "length": 17}, #Ex: 4015202031314545
            "TRANSACTION_TYPE": {"type": str, "length": [5, 6], "options": ["DEBIT", "CREDIT"]}, #Ex: DEBIT
            "POST_DATE": {"type": str, "length": 8}, #YYYYMMDD Ex: 20240101
            "TRANSACTION_AMOUNT": {"type": str, "length": [0, 16]}, #Ex: 200
            "DESCRIPTION": {"type": str, "length": [0, 1000]},
            "ITEM_NUMBER": {"type": str, "length": [0, 3]}, #Ex: 30
            "TRANSACTION_DATE": {"type": str, "length": 8}, #YYYYMMDD Ex: 20240101
            "TRANSACTION_MONTH": {"type": str, "length": 2}, #Ex: 05
        }
        
        
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