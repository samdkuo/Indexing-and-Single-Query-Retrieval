import json

file_directory = "WEBPAGES_RAW/bookkeeping.json"

json_data=open(file_directory).read()

class json_parse():

    json_data

    def __init__(self, jsonFile):
        json1_file = open(jsonFile)
        json1_str = json1_file.read()
        self.json_data = json.loads(json1_str)

    def result(self):
        return self.json_data
