import os.path, re, operator 
from BeautifulSoup import BeautifulSoup, Comment 
from HTMLParser import HTMLParser
from collections import defaultdict

'''iterate through files'''
def iterate_files():
    for dir in range(0, 1):
        for f in range(0, 500):
            file = "WEBPAGES_RAW/" + str(dir) +"/" + str(f)
            if os.path.isfile(file):
                print file

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
    word_freq = sorted(word_freq.iteritems(), key=operator.itemgetter(1), reverse=True)

    return word_freq

      
parse_html("WEBPAGES_RAW/0/2")
'''input tokens into db'''
def insert_tokens(dict):
  print "here"


