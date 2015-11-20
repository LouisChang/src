import json
import itertools
from itertools import islice
import codecs
import os
import time

def read_tweets():
   
    data = []	
    try:
        with open(os.path.dirname(__file__) +  '/../tweet_input/tweets.txt') as f:
            for line in f:
                jfile = json.loads(''.join(line))
                data.append(jfile)
        return data
    except:
        continue
	
def clean_tweets(data):
    
    count = 0
    f = open(os.path.dirname(__file__) +  '/../tweet_output/ft1.txt','w')
    for item in data:
        if item.get('text'):
            string=item['text'].encode('ascii','ignore')+' (timestamp: '+item['created_at']+')\n'
            f.write(string)
            if item['text'].encode('ascii','ignore')!=item['text']:
                count=count+1
    f.write('\n')
    string=str(count)+' tweets contained unicode.'
    f.write(string)
    f.close()

def main():
    data = read_tweets()
    clean_tweets(data)

if __name__ == "__main__":
    main()