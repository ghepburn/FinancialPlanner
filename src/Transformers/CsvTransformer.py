import json

from .BaseTransformer import BaseTransformer

class CsvTransformer(BaseTransformer): 


    def csvToObject(self, csv):
        result = []

        for row in csv:
            dict = json.dumps(csv)
            result.append(dict)

        return result