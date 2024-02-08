

class BaseTransformer:
    def __init__(self, logger, configs):
        self.logger = logger
        self.configs = configs
    
    def transform(self, item):
        pass