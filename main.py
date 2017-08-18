# -*- coding: utf-8 -*-
#! /usr/bin/env python
"""
main.py
"""
from konlpy.tag import Kkma 
from konlpy.utils import pprint
import numpy as np
import sys
import codecs
import os
import json 
"""
!!! Need to reduce look-up time!
==> Sol: Process the corpora into dictionary word: # of docs the word appears in 
Design Choice:
    How to compute IDF?
    Option 1: Have a precomputed list
    Option 2: Compute on the fly - will take too much time
Inverse Document Frequency = # of occuring docs / # of all docs
(1) Need to read from the corpora
(2) Have a frequency list

total_num = 60075
"""

def usage():
    print "need 2 args: inputfile and # of summary sentences"

def query_word(word):
    """
    Takes in a word, returns the number of docs that word occurs
    """
    #kkma = kk()   
    basedir = "./corpora/all/"
    files = os.listdir(basedir)
    
    total_num = 0
    doc_count = 0
    
    word_count = 0
    for txt in files:
        with codecs.open(basedir+txt, "r", "utf-8") as f:
            for line in f:
                if line == "@DOCUMENT\n":
                    word_found = 0
                    doc_count = 0
                    total_num += 1
                else:
                    doc_count += 1
                if doc_count >= 6:
                    if not word_found:
                    #print line
                    #pprint(kkma.pos(line))
                    #pprint(line.split())
                        wordlist = line.split()
                        for item in wordlist:
                            #print type(word)
                            #print type(item)
                            if word == item and not word_found:
                                word_found = 1
                                word_count += 1
    #print word_count
    return word_count

def get_idf(stat, word):
    total_num = 60075.0
    if word not in stat:
        return 0
    else:
        word_count = stat[word]#query_word(word)
    #if word_count == 0:
    #    return 0 
    return np.log(total_num/word_count)

def get_count(text, word):
    word_count = 0.0
    total_words = 0.0
    for item in text:
        total_words += 1.0
        if word == item:
            word_count += 1.0
    return word_count 

def get_tf(text, word):
    #print "gettf"
    #print text
    
    total_words = len(text)
    return get_count(text, word)/total_words

def get_score(stat, text, sentence):
    #print "getscore"
    #print text
    #print sentence

    score = 0.0
    split_text = text.split()
    word_list = sentence.split()
    for word in word_list:
        score += get_tf(split_text, word) * get_idf(stat, word)
    return score

def main():
    """
    print "Writing stat file to json..."
    stat = {}
    basedir = "./corpora/all/"
    files = os.listdir(basedir)
    
    total_num = 0
    doc_count = 0
    
    for txt in files:
        with codecs.open(basedir+txt, "r", "utf-8") as f:
            for line in f:
                if line == "@DOCUMENT\n":
                    found_list = set()
                    word_found = 0
                    doc_count = 0
                    total_num += 1
                else:
                    doc_count += 1
                if doc_count >= 6:
                    wordlist = line.split()
                    for item in wordlist:
                        if item not in found_list:
                            if item not in stat:
                                stat[item] = 1
                            else:
                                stat[item] += 1
                        found_list.add(item)
                        pass

    with open('stat.json', 'w') as fp:
        json.dump(stat, fp)
    print "Finished writing stat file to json..."
    for item in stat:
        pprint(item)
        pprint(stat[item])
    """

    if len(sys.argv) != 3:
        usage()
        exit()
    else:
        inputfile = sys.argv[1]
        nums = int(sys.argv[2])
        
        #reading json file
        with open('stat.json', 'r') as fp:
            stat = json.load(fp)
            
            kkma = Kkma()
            text = codecs.open(inputfile, "r", "utf-8") 
               
            text_string = text.read()
            sentences = kkma.sentences(text_string)
            scores = []
            for sentence in sentences:
                scores.append(get_score(stat, text_string, sentence))
       
            indices = sorted(range(len(scores)), key = lambda k: scores[k])
            indices.reverse()
               
            final_sentences = []
            for i in range(nums):
                final_sentences.append(indices[i])
            
            print "printing..."
            #print sentences
            #print final_sentences

            for i in range(len(sentences)):
                if i in final_sentences:
                    pprint(sentences[i])

            text.close()
     
        """
        kkma = Kkma()
        text = codecs.open(inputfile, "r", "utf-8") 
               
        text_string = text.read()
        sentences = kkma.sentences(text_string)
        scores = []
        for sentence in sentences:
            scores.append(get_score(text_string, sentence))
       
        indices = sorted(range(len(scores)), key = lambda k: scores[k])
        indices.reverse()
               
        final_sentences = []
        for i in range(nums):
            final_sentences.add([indices[i]])
        
        for i in range(len(sentences)):
            if i in final_sentences:
                pprint(sentences[i])

        text.close()
        """
    return

if __name__ == "__main__":
    main()
