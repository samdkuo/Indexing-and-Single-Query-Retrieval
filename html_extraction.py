import os.path
from BeautifulSoup import BeautifulSoup, Comment 

'''iterate through files'''
def iterate_files():
    for dir in range(0, 1):
        for f in range(0, 500):
            file = "WEBPAGES_RAW/" + str(dir) +"/" + str(f)
            if os.path.isfile(file):
                print file

'''parse html; tokenize; return dictionary'''
def parse_html(path_name):
    with open(path_name, "r") as data:
        soup = BeautifulSoup(data.read())
        comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        [comment.extract() for comment in comments] 
        print soup.text


parse_html("WEBPAGES_RAW/0/1")
'''input tokens into db'''
def insert_tokens(dict):
  print "here"


