from json_parse import json_parse
import html_extraction.py
import sys
import os.path

def main():
    total_urls = json_parse("WEBPAGES_RAW/bookkeeping.json")
    if not os.path.isfile("index.txt"):
      iterate_files()
    docs = search("irvine")
    for d in docs:
        print(total_urls.get_url(d))

def search(term):
    docs = []
    file = open("index.txt", "r")
    for line in file:
        i = 0
        tokens = line.split("-")
        word = tokens[0]
        if term == word:
            posting_list = tokens[1].split(",")
            for pair in posting_list:
                if len(pair) > 0:
                    i += 1
                    doc_id = pair.split(":")[0]
                    docs.append(doc_id)
                    if i >= 10:
                        file.close()
                        return docs

if __name__ == "__main__":
    main()
