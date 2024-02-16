

import json
import datetime

class Configs:
    values = {
        # Behaviour
        "USE_TEST_FILE": False, # Will retreive TEST_GOOGLE_DRIVE_FILE_ID rather then retreieve all files
        "USE_CACHE": False, # Will not retreive files from Google Drive if we have them stored
        "LOG_DEBUG": True,
        "LOG_TO_FILE": True,

        # Confgurations
        "LOCAL_DATA_DIRECTORY": "./data",
        "LOCAL_DATA_FILE_NAME": "data.csv",
        "ERROR_FILE": "./logs/",
        "LOG_FILE": "./logs/",
        "GOOGLE_DRIVE_DIRECTORY_PATH": [],
        "DESIRED_GOOGLE_DRIVE_DOWNLOADED_FILE_TYPE": "text/csv",
        "TEST_GOOGLE_DRIVE_FILE_ID": "",
        "CHARACTERS_TO_REMOVE": ["\"", "'", "[", "]", "\r", "  "],
        
        "SUPPORTED_FILE_TYPES": [],

        # File Column Mappings
        "BMO_CHEQUINGS_COLUMNS": ["CARD_NUMBER", "TRANSACTION_TYPE", "POST_DATE", "TRANSACTION_AMOUNT", "DESCRIPTION"],
        "BMO_CREDIT_CARD_COLUMNS": ["ITEM_NUMBER", "CARD_NUMBER", "TRANSACTION_DATE", "POST_DATE", "TRANSACTION_AMOUNT", "DESCRIPTION"],

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
            "SOURCE": {"type": str, "length":[1, 15]} #SUPPORT_FILE_TYES enum Ex: BMO_CHEQUINGS
        },

        "INTERCHANGEABLE_COLUMNS": {
            "POST_DATE": "TRANSACTION_DATE",
            "TRANSACTION_DATE": "POST_DATE"
        },

        # Desired Format
        "OUTPUT_COLUMNS": ["SOURCE", "TRANSACTION_DATE", "TRANSACTION_AMOUNT", "DESCRIPTION"]
    }
    
    def __init__(self):
        self.dateToday = datetime.datetime.today().strftime('%Y%m%d')
        self.timestamp = str(datetime.datetime.now()).replace(" ", "").replace("-", "").replace(":", "").replace(".", "")

        self.loadDynamicConfigs()
        self.loadSecrets()

    def loadDynamicConfigs(self):
        print("Configs.loadDynamicConfigs()")
        self.values["LOG_FILE"] = self.values["LOG_FILE"] + self.timestamp + ".log"
        self.values["ERROR_FILE"] = self.values["ERROR_FILE"] + "errors." + self.timestamp + ".log"


    def loadSecrets(self):
        print("Configs.loadSecrets()")
        
        f = open("secrets.json", "r")
        jsonSecrets = f.read()
        secrets = json.loads(jsonSecrets)
        
        for key in secrets.keys():
            self.values[key] = secrets[key]

        print("Configs.loadSecrets() Secrets Set")
        
    def get(self, name):
        try:
            return self.values[name]
        except Exception as e:
            print("Error name config does not exist. ", e)