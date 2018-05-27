import json

class json_parse():
    def __init__(self, jsonFile):
        file = open(jsonFile)
        data = file.read()
        self.json_data = json.loads(data)
    
    def result(self):
        return self.json_data

    def get_url(self, key):
        return self.json_data[key].encode("ascii", "ignore").decode("utf-8")


