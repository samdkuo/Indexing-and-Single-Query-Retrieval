from json_parse import json_parse
import html_extraction, sys, os.path, tf_idf_calculation, operator
from flask import Flask, render_template, requesu

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
        for d, w in docs:
            print d, " ", w
            print(str(count) +". " + total_urls.get_url(d))
            count += 1
        if not docs:
            print("UNABLE TO FIND QUERY")
        print("\nINPUT Q TO STOP SEARCHING")

def search(query):
    terms = query.strip().split(" ")
    if len(terms) == 1:
        return search_one(terms[0])[:10]

    docs_list = []
    for term in terms:
      docs_list.append(search_one(term))

    docs_list.sort(key=len)
    current = docs_list[0]
    docs_list.remove(current)

    for docs in docs_list:
        current = compare_and(current, docs)
        if len(current) > len(docs):
            docs_list.append(current)
            current = docs

    return current[:10]

def compare_or(first, second):
    combined = []
    while first and second:
        d1 = first[0]
        d2 = second[0]
        if d1[1] > d2[1]:
            combined.append(d1)
            first.remove(d1)
        else:
            combined.append(d2)
            second.remove(d2)
    if first:
        combined.extend(first)
    elif second:
        combined.extend(second)
    return combined
    
def compare_and(first, second):
    matched = []
    while first and second:
        d1 = first[0]
        d2 = second[0]
        if d1[0] == d2[0]:
            matched.append(d1)
            first.remove(d1)
            second.remove(d2)
        elif d1[1] > d2[1]:
            first.remove(d1)
        else:
            second.remove(d2)
    
    if not matched:
        return compare_or(first, second)
    
    return matched

def search_one(term):
    docs = {}
    file = open("tf_idf_index.txt", "r")
    for line in file:
        i = 0
        tokens = line.split("-")
        word = tokens[0]
        if term == word:
            posting_list = tokens[1].split(",")
            for pair in posting_list:
                if len(pair) > 0:
                    doc_id = pair.split(":")[0]
                    weight = pair.split(":")[1]
                    docs[doc_id] = weight
            file.close()
            break
    return sorted(docs.iteritems(), key=operator.itemgetter(1), reverse=True)


app = Flask(__name__)
total_urls = json_parse("WEBPAGES_RAW/bookkeeping.json")

formHtml = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Search</title>
</head>
<body>
    <form action = "http://localhost:5000/result" method = "POST">
         <p>Search <input type = "text" name = "Search" /></p>
         <p><input type = "submit" value = "submit" /></p>
      </form>
</body>
</html>
"""

@app.route('/')
def searchPage():
    if not os.path.isfile("index.txt"):
        html_extraction.iterate_files()

    if not os.path.isfile("tf_idf_index.txt"):
        tf_idf_calculation.loop_thru_file()
    return formHtml

@app.route('/result',methods = ['POST', 'GET'])
def result():
   return_string = ""
   if request.method == 'POST':
      result_dict = request.form
      result = ""
      for k,v in result_dict.items():
          result = v
      print(result)
      query = result.lower()
      docs = search(query)
      count = 1
      for d in docs:
          return_string += str(count) + ". " + total_urls.get_url(d) + "<br>"
          count += 1
      if not docs:
          return_string =  "UNABLE TO FIND QUERY"
      
      return return_string


if __name__ == "__main__":
    app.run()
   # main()
