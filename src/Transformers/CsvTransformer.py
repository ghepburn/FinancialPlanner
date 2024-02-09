from .BaseTransformer import BaseTransformer

class CsvTransformer(BaseTransformer): 


    def csvToObject(self, csv):
        self.logger.debug("CsvTransformer.csvToObject()")

        data = []
       
        rows = csv.split("\n")
        for row in rows:
            rowData = row.split(",")
            data.append(rowData)

        return data