import json

class Logger:
    def objToString(self, obj):
       jsonObj = json.dumps(obj)
       return jsonObj

    def debug(self, message):
        if type(message) is not str:
            message = self.objToString(message)

        message = "DEBUG: " + message
        print(message)

    def info(self, message):
        if type(message) is not str:
            message = self.objToString(message)

        message = "INFO: " + message
        print(message)

    def error(self, message, exception=None):
        if type(message) is not str:
            message = self.objToString(message)

        message = "ERROR: " + message
        print(message)
        if exception:
            print(exception)
    