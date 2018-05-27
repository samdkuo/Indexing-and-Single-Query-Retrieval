from collections import defaultdict
import math, operator

def tf_idf(term_dict):
    tf_idf_dict = defaultdict(float)
    N = 37497 # size of corpus
    d = len(term_dict)
    for key,value in term_dict.items():
        tf_weight = 1 + math.log(value)
        idf_weight = math.log(N/d)
        weight = tf_weight * idf_weight
        tf_idf_dict[key] = weight
    sorted_tf_idf = sorted(tf_idf_dict.items(), key=operator.itemgetter(1), reverse = True)
    return sorted_tf_idf

def loop_thru_file():
    file = open("index.txt", "r")
    tf_idf_file = open("tf-idf_index.txt", "w")
    for line in file:
        term_dict = defaultdict(int)
        tokens = line.split("-")
        term = tokens[0]
        doc_freq_pairs = tokens[1].split(",")
        for pair in doc_freq_pairs:
            if len(pair) > 1:
                items = pair.split(":")
                doc = items[0]
                freq = items[1]
                term_dict[doc] = int(freq)
        sorted_tf_idf = tf_idf(term_dict)
        new_line = term + "-"
        for key, value in sorted_tf_idf:
            new_line += key + ":" + str(value) + ","
        tf_idf_file.write(new_line[:-1] + "\n")
    file.close()
    tf_idf_file.close()

loop_thru_file()
        
            
        
        
    
                
                
    
