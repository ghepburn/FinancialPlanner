import json
import os
import datetime

class Logger:
    def __init__(self, configs):
        self.configs = configs
        self.logDebug = self.configs.get("LOG_DEBUG")
        self.logFileName = self.configs.get("LOG_FILE")
        self.errorFileName = self.configs.get("ERROR_FILE")
        self.logToFile = self.configs.get("LOG_TO_FILE")

    def objToString(self, obj):
       jsonObj = json.dumps(obj)
       return jsonObj
    
    def log(self, message):
        if self.logToFile:
            message = str(datetime.datetime.now()) + " - " + message
            if os.path.isfile(self.logFileName):
                file = open(self.logFileName, 'a')
                file.write("\n")
                file.write(message)
                file.close()
            else:
                file = open(self.logFileName, 'w')
                file.write(message)
                file.close()
        else:
            print(message)

    def debug(self, message):
        if self.logDebug:
            if type(message) is not str:
                message = self.objToString(message)

            message = "DEBUG: " + message
            self.log(message)

    def info(self, message):
        if type(message) is not str:
            message = self.objToString(message)

        message = "INFO: " + message
        self.log(message)

    def error(self, message, exception=None):
        if type(message) is not str:
            message = self.objToString(message)

        message = "ERROR: " + message
        self.log(message)
        if exception:
            self.log(str(exception))

    def captureError(self, exception, params):
        self.debug("Logger.captureError()")
        error = str(datetime.datetime.now()) + " - " + str(exception) + " - " + json.dumps(params)

        if os.path.isfile(self.errorFileName):
            file = open(self.errorFileName, 'a')
            file.write("\n")
            file.write(error)
            file.close()
        else:
            file = open(self.errorFileName, 'w')
            file.write(error)
            file.close()

    def getCapturedErrors(self):
        if self.logDebug:
            self.debug("Logger.getCapturedErrors()")

            if os.path.isfile(self.errorFileName):
                file = open(self.errorFileName, 'r')
                self.debug(file.read())
                file.close()
    