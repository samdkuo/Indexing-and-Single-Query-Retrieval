from json_parse import json_parse

def main():
    json_data = json_parse("WEBPAGES_RAW/bookkeeping.json").result()
    print(json_data["0/0"]) #for testing purposes

if __name__ == "__main__":
    main()