import json

file_directory = "WEBPAGES_RAW/bookkeeping.json"

json_data=open(file_directory).read()

class json_parse():

    json_data = dict()

    def __init__(self, jsonFile):
        json1_file = open(jsonFile)
        json1_str = json1_file.read()
        self.json1_data = json.loads(json1_str)[0]

    def result(self):
        return json_data
