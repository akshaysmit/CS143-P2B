#!/usr/bin/env python

"""Clean comment text for easier parsing."""

from __future__ import print_function

import re
import string
import argparse
import sys
import bz2
import json
from pprint import pprint

__author__ = ""
__email__ = ""

# Some useful data.
_CONTRACTIONS = {
    "tis": "'tis",
    "aint": "ain't",
    "amnt": "amn't",
    "arent": "aren't",
    "cant": "can't",
    "couldve": "could've",
    "couldnt": "couldn't",
    "didnt": "didn't",
    "doesnt": "doesn't",
    "dont": "don't",
    "hadnt": "hadn't",
    "hasnt": "hasn't",
    "havent": "haven't",
    "hed": "he'd",
    "hell": "he'll",
    "hes": "he's",
    "howd": "how'd",
    "howll": "how'll",
    "hows": "how's",
    "id": "i'd",
    "ill": "i'll",
    "im": "i'm",
    "ive": "i've",
    "isnt": "isn't",
    "itd": "it'd",
    "itll": "it'll",
    "its": "it's",
    "mightnt": "mightn't",
    "mightve": "might've",
    "mustnt": "mustn't",
    "mustve": "must've",
    "neednt": "needn't",
    "oclock": "o'clock",
    "ol": "'ol",
    "oughtnt": "oughtn't",
    "shant": "shan't",
    "shed": "she'd",
    "shell": "she'll",
    "shes": "she's",
    "shouldve": "should've",
    "shouldnt": "shouldn't",
    "somebodys": "somebody's",
    "someones": "someone's",
    "somethings": "something's",
    "thatll": "that'll",
    "thats": "that's",
    "thatd": "that'd",
    "thered": "there'd",
    "therere": "there're",
    "theres": "there's",
    "theyd": "they'd",
    "theyll": "they'll",
    "theyre": "they're",
    "theyve": "they've",
    "wasnt": "wasn't",
    "wed": "we'd",
    "wedve": "wed've",
    "well": "we'll",
    "were": "we're",
    "weve": "we've",
    "werent": "weren't",
    "whatd": "what'd",
    "whatll": "what'll",
    "whatre": "what're",
    "whats": "what's",
    "whatve": "what've",
    "whens": "when's",
    "whered": "where'd",
    "wheres": "where's",
    "whereve": "where've",
    "whod": "who'd",
    "whodve": "whod've",
    "wholl": "who'll",
    "whore": "who're",
    "whos": "who's",
    "whove": "who've",
    "whyd": "why'd",
    "whyre": "why're",
    "whys": "why's",
    "wont": "won't",
    "wouldve": "would've",
    "wouldnt": "wouldn't",
    "yall": "y'all",
    "youd": "you'd",
    "youll": "you'll",
    "youre": "you're",
    "youve": "you've"
}

# You may need to write regular expressions.

def sanitize(text):
    """Do parse the text in variable "text" according to the spec, and return
    a LIST containing FOUR strings 
    1. The parsed text.
    2. The unigrams
    3. The bigrams
    4. The trigrams
    """

    #Replace newline/tab with space
    str = text.replace("\\n", " ")
    str = str.replace("\\t", " ")

    #Replace URLs with empty string
    obj = re.search(r'\[([^\]]*)\]\s?\([^\)]*\)', str)
    while obj:
        found = obj.group(1)
        str = re.sub(r'\[[^\]]*\]\s?\([^\)]*\)', found, str, 1)
        obj = re.search(r'\[([^\]]*)\]\s?\([^\)]*\)', str)
        
    str = re.sub(r'https?:\/\/[^\s]+', '', str)
    str = re.sub(r'www\.[^\s]+', '', str)
    
    #Split text on spaces or external punctuation
    tokens1 = str.split()

    #Separate external punctuation into separate tokens
    tokens2 = [] 
    for t in tokens1:
        obj = re.search('^([^\w]+)', t)
        if obj:
            found = obj.group(1)
            for i in range (0, len(found)):
                tokens2.append(found[i])
            t = t[len(found):]
            
        obj = re.search('([^\w]+)$', t)
        
        if obj:
            found = obj.group(1)
            t = t[:len(t)-len(found)]
            tokens2.append(t)
            for i in range (0, len(found)):
                tokens2.append(found[i])
        else:
            tokens2.append(t)

    #Remove special characters/punctuations except ending/embedded. Also change to lowercase
    single_quote = False 
    tokens3 = []
    for t in tokens2:
        t = t.lower()
        if len(t) >= 2:
            if single_quote:     #hardcoded contractions that would cause problems
                if t == "tis":
                    t = "'tis"
                elif t == "ol":
                    t = "'ol"
                single_quote = False
            tokens3.append(t)
            continue

        obj = re.search('^\w$', t)
        if obj:
            tokens3.append(t)
        
        obj = re.search('^[!?\.,;:]$', t)
        if obj:
            tokens3.append(t)

        if t == "'":
            single_quote = True

    parsed_text = ""
    unigrams = ""
    for t in tokens3:
        parsed_text = parsed_text + t + " "
        if not re.search('^[!?\.,;:]$', t):
            unigrams = unigrams + t + " "
    if unigrams != "":
        unigrams = unigrams[:-1]
    if parsed_text != "":
        parsed_text = parsed_text[:-1]
        
    bigrams = ""
    i = 0
    j = 1
    while j < len(tokens3):
        if not re.search('^[!?\.,;:]$', tokens3[i]) and not re.search('^[!?\.,;:]$', tokens3[j]):
            bigrams += tokens3[i] + "_" + tokens3[j] + " "
        i = i+1
        j = j+1
    if bigrams	!= "":
        bigrams = bigrams[:-1]
        
    trigrams = ""
    i = 0
    j = 1
    k = 2
    while k < len(tokens3):
        if not re.search('^[!?\.,;:]$', tokens3[i]) and not re.search('^[!?\.,;:]$', tokens3[j]) \
           and not re.search('^[!?\.,;:]$', tokens3[k]):
            trigrams += tokens3[i] + "_" + tokens3[j] + "_" + tokens3[k] + " "
        i = i+1
        j = j+1
        k = k+1
    if trigrams	!= "":
        trigrams = trigrams[:-1]

    return [parsed_text, unigrams, bigrams, trigrams]


if __name__ == "__main__":
    # This is the Python main function.
    # You should be able to run
    # python cleantext.py <filename>
    # and this "main" function will open the file,
    # read it line by line, extract the proper value from the JSON,
    # pass to "sanitize" and print the result as a list.

    #the json extraction code is from
    #https://stackoverflow.com/questions/20400818/python-trying-to-deserialize-multiple-json-objects-in-a-file-with-each-object-s
    filename = sys.argv[1]
    if filename.endswith('.json'):
        with open(filename, "r") as f:
            for line in f:
                while True:
                    try:
                        jfile = json.loads(line)
                        print (sanitize(jfile["body"]))
                        break
                    except ValueError:
                        # Not yet a complete JSON value
                        line += next(f)
                        
    elif filename.endswith('.bz2'):
        f = bz2.BZ2File(filename, "r")
        for line in f:
            while True:
                try:
                    jfile = json.loads(line)
                    print (sanitize(jfile["body"]))
                    break
                except ValueError:
                    # Not yet a complete JSON value                       
                    line += next(f)
