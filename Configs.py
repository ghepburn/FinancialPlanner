

import json

class Configs:
    values = {
        "LOCAL_DATA_DIRECTORY": "./data",
        "LOCAL_DATA_FILE_NAME": "data.csv",
        "GOOGLE_DRIVE_DIRECTORY_PATH": [],
        "DESIRED_GOOGLE_DRIVE_DOWNLOADED_FILE_TYPE": "text/csv",
        "TEST_GOOGLE_DRIVE_FILE_ID": "",
        "CHARACTERS_TO_REMOVE": ["\"", "'", "[", "]", "\r", "  "],
        
        "SUPPORTED_FILE_TYPES": [
            "BMO_CHEQUINGS", 
            "BMO_CREDIT_CARD"
        ],

        # File Column Mappings
        "BMO_CHEQUINGS_COLUMNS": ["CARD_NUMBER", "TRANSACTION_TYPE", "POST_DATE", "TRANSACTION_AMOUNT", "DESCRIPTION"],
        "BMO_CREDIT_CARD_COLUMNS": ["ITEM_NUMBER", "CARD_NUMBER", "TRANSACTION_DATE", "TRANSACTION_MONTH", "POST_DATE", "TRANSACTION_AMOUNT", "DESCRIPTION"],

        # Column Details
            # Type: Python type - Example: str
            # Length: Expected length or expected min and max range. -- Example: 5 or [1, 10] (min 1 max 10)
        "COLUMN_DETAILS": {
            "CARD_NUMBER": {"type": str, "length": 17}, #Ex: 4015202031314545
            "TRANSACTION_TYPE": {"type": str, "length": [5, 6], "options": ["DEBIT", "CREDIT"]}, #Ex: DEBIT
            "POST_DATE": {"type": str, "length": 8}, #YYYYMMDD Ex: 20240101
            "TRANSACTION_AMOUNT": {"type": str, "length": [1, 16]}, #Ex: 200
            "DESCRIPTION": {"type": str, "length": [0, 1000]},
            "ITEM_NUMBER": {"type": str, "length": [0, 3]}, #Ex: 30
            "TRANSACTION_DATE": {"type": str, "length": 8}, #YYYYMMDD Ex: 20240101
            "TRANSACTION_MONTH": {"type": str, "length": 2}, #Ex: 05
            "SOURCE": {"type": str, "length":[1, 15]} #SUPPORT_FILE_TYES enum Ex: BMO_CHEQUINGS
        },

        "INTERCHANGEABLE_COLUMNS": {
            "POST_DATE": "TRANSACTION_DATE",
            "TRANSACTION_DATE": "POST_DATE"
        },

        # Desired Format
        "OUTPUT_COLUMNS": ["SOURCE", "TRANSACTION_DATE", "TRANSACTION_AMOUNT", "DESCRIPTION"]
        
        
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