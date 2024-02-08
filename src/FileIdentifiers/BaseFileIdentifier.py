

class BaseFileIdentifier:

    def __init__(self, logger, configs):
        self.logger = logger
        self.configs = configs
        
    def getFileType(self, file):
        return None