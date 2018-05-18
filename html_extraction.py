import os.path, re, operator, pymongo
from BeautifulSoup import BeautifulSoup, Comment
from HTMLParser import HTMLParser
from collections import defaultdict
from pymongo import MongoClient

client = MongoClient()
db = client.IndexDB
collection = db.word_collection

'''iterate through files'''
def iterate_files():
    for dir in range(0, 1):
        for f in range(8, 10):
            key = str(dir) +"/" + str(f)
            file = "WEBPAGES_RAW/" + key 
            if os.path.isfile(file):
                tokens = parse_html(file)
                insert_tokens(key, tokens)


'''parse html; tokenize; return dictionary'''
def parse_html(path_name):
    content = []
    with open(path_name, "r") as data:
        soup = BeautifulSoup(data.read())
        comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        [comment.extract() for comment in comments] 
        [script.extract() for script in soup("script")]
        [style.extract() for style in soup("style")] 
        content = " ".join(item.strip() for item in soup.findAll(text=True))
        content = HTMLParser().unescape(content)
        content = content.encode("ascii", "ignore")

    pattern = re.compile('[\W_]+')
    content = pattern.sub(' ', content).lower().split()
  
    word_freq = defaultdict(int)
    for word in content:
        word_freq[word] += 1
    return word_freq

      
'''input tokens into db'''
def insert_tokens(doc_id, tokens):
    for word, freq in tokens.items():
        result = collection.update_one(
            {"id": word},
            {"$set" : {"$inc" : {"freq" : freq}}},
            {"$push" : {"docs" : doc_id}})
        print(doc_id, tokens)


iterate_files()
