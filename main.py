from json_parse import json_parse
import html_extraction, sys, os.path, tf_idf_calculation

def main():
    total_urls = json_parse("WEBPAGES_RAW/bookkeeping.json")
    if not os.path.isfile("index.txt"):
        html_extraction.iterate_files()
    
    if not os.path.isfile("tf_idf_index.txt"):
        tf_idf_calculation.loop_thru_file() 

    while True:
        query = raw_input("search: ").lower()
        if query == "q":
            break
        docs = search(query)
        count = 1
        try:
            for d in docs:
                print(str(count) +". " + total_urls.get_url(d))
                count += 1
        except:
            print("UNABLE TO FIND QUERY")
        print("\nINPUT Q TO STOP SEARCHING")

def search(query):
    terms = query.split(" ")
    if len(terms) == 1:
        return search_one(terms[0])[:10]

    docs_list = []
    for term in terms:
      docs_list.append(search_one(term))

    docs_list.sort(key=len)
    matched = docs_list[0]
    docs_list.remove(matched)

    for docs in docs_list:
        matched = compare(matched, docs)

    return matched[:10]
    
def compare(first, second):
    match = []
    while first and second:
        d1 = first[0]
        d2 = second[0]
        if d1 == d2:
            match.append(d1)
            first.remove(d1)
            second.remove(d2)
        elif d1 < d2:
            first.remove(d1)
        else:
            second.remove(d2)
    return match

def search_one(term):
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
                    doc_id = pair.split(":")[0]
                    docs.append(doc_id)
            file.close()
            break
    return docs

if __name__ == "__main__":
    main()
