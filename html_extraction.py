import os.path, re, operator, shutil, codecs
try:
    from bs4 import BeautifulSoup, Comment
    from html.parser import HTMLParser
except:
    from BeautifulSoup import BeautifulSoup, Comment
    from HTMLParser import HTMLParser
from collections import defaultdict
from shutil import copyfile

'''iterate through files'''
def iterate_files():
    for d in range(0, 75):
        print("In directory " + str(d))
        folder_dict = parse_html(d)
        new_terms = add_existing_terms_to_index(folder_dict)
        add_new_terms_to_index(new_terms)


'''parse html; tokenize; return dictionary'''
def parse_html(d):
    folder_dict = defaultdict(dict)
    for f in range(0, 500):
        #print("In file " + str(f))
        key = str(d) +"/" + str(f)
        file = "WEBPAGES_RAW/" + key
        
        if os.path.isfile(file):
            content = []
            with codecs.open(file, "r", encoding="utf-8") as data:
                data = data.read().encode("ascii", "ignore")
                soup = BeautifulSoup(data)
                comments = soup.findAll(text=lambda text:isinstance(text, Comment))
                [comment.extract() for comment in comments] 
                [script.extract() for script in soup("script")]
                [style.extract() for style in soup("style")] 
                content = " ".join(item.strip() for item in soup.findAll(text=True))
                content = HTMLParser().unescape(content)
                content = content.encode("ascii", "ignore")
                content = content.decode('utf-8')

            pattern = re.compile('[\W_]+')
            content = pattern.sub(' ', content).lower().split()
  
            for word in content:
                if len(word) > 1:
                    if word not in folder_dict:
                        folder_dict[word] = defaultdict(int)
                    folder_dict[word][key] +=1
    return folder_dict

def add_existing_terms_to_index(folder_dict):
    try:
        file = open("index.txt", "r")
        temp = open("temp.txt", "w")
        for line in file:
            tokens = line.split("-")
            term = tokens[0]
            if term in folder_dict:
                new_line = ""
                for doc_id, freq in folder_dict[term].items():
                    new_line += "," + doc_id + ":" + str(freq)
                temp.write(line.rstrip("\n") + new_line + "\n")
                folder_dict.pop(term)
            else:
                temp.write(line)
        file.close()
        temp.close()
        shutil.copyfile("temp.txt", "index.txt")
        os.remove("temp.txt")
    finally:
        return folder_dict

def add_new_terms_to_index(new_terms):
    file = open("index.txt","a")
    for term in new_terms:
        new_line = ""
        for doc_id, freq in new_terms[term].items():
            new_line += doc_id + ":" + str(freq) + ","
        file.write(term + "-" + new_line + "\n")
    file.close()

    
