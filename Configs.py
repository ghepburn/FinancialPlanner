


class Configs:
    values = {
        "LOCAL_DATA_DIRECTORY": "./data",
        "GOOGLE_DRIVE_DIRECTORY_PATH": ["Finances", "Data"],
        "DESIRED_GOOGLE_DRIVE_DOWNLOADED_FILE_TYPE": "text/csv",
        "TEST_GOOGLE_DRIVE_FILE_ID": "1-3bXrXYz-XBwQw4n-2f8okSoAkcSc_fzDTEPIa2fG6s",
        
        # Financial File Types
        "FINANCIAL_FILE_TYPES": [
            "BMO_CHEQUINGS_FILE_TYPE", 
            "BMO_CREDIT_CARD_FILE_TYPE"
        ],

        # Column Mapping
        
        
    }
    
    def __init__(self, logger):
        self.logger = logger
        
    def get(self, name):
        try:
            return self.values[name]
        except Exception as e:
            self.logger.error("Error name config does not exist. ", e)