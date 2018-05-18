from json_parse import json_parse

def main():
    total_urls = json_parse("WEBPAGES_RAW/bookkeeping.json")
    print total_urls.get_url("0/0") #for testing purposes


if __name__ == "__main__":
    main()
