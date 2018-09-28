import json
import re 
import operator
from collections import Counter

import nltk 
nltk.download('stopwords')

from nltk.corpus import stopwords
import string
from nltk import bigrams 
 

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

from flask import Flask

app = Flask(__name__)

@app.route("/")

def hello():


    tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
    emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
    
    def tokenize(s):
        return tokens_re.findall(s)
    
    def preprocess(s, lowercase=False):
        tokens = tokenize(s)
        if lowercase:
            tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens
    
    punctuation = list(string.punctuation)
    #stop = stopwords.words('english') + punctuation + ['rt', 'via', 'RT', '\'', 'session', '#MSIgnite', 'Microsoft', '#msignite', 'The', 'I', 'because', '’', '…', '2019', 'This', 'A']

    stop = stopwords.words('english') + punctuation + ['rt', 'via', 'RT', '\'', 'session', '#MSIgnite', 'Microsoft', '#msignite', 'The', 'I', 'because', '’', '…', '2019', 'This', 'A']


    with open('python.json', 'r') as f:
        count_all = Counter()
        count_filtered = Counter()
        count_bigrams = Counter()
        for line in f:
            if len(line.strip()) > 0:
                tweet = json.loads(line)
                #tokens = preprocess(tweet['text'])
                terms_all = [term for term in preprocess(tweet['text'])]
                terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]
                # Update the counter
                count_all.update(terms_all)
                
                if len(terms_stop) > 0:
                    count_filtered.update(terms_stop)
                    terms_bigram = bigrams(terms_stop)
                    listitems = list(terms_bigram) 
                    count_bigrams.update(listitems)

        result = '<html><body>'

        result += '<b>Most common words: </b><br><br>'

        for x in count_filtered.most_common(10)[:]:
            #if len(x)==3:
            result += str(x)
            result += '<br>'
        

        result += '<br><br><b>Most common word pairs: </b><br>'
        #print(count_filtered.most_common(10))
        for x in count_bigrams.most_common(10)[:]:
            #if len(x)==3:
            result += str(x)
            result += '<br>'
        #return str(count_bigrams.most_common(10))


        result += '</body></html>'
        return result