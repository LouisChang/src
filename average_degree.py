import json
import os
import time
import scipy as sp

# remove older twittes
def remove_edges(graph, expired_hashtag):
    connected_hashtags = graph[expired_hashtag]
    for hashtag in connected_hashtags:
        graph[hashtag].remove(expired_hashtag)
    del graph[expired_hashtag]
    return graph

start_time = time.time()
input_dir = "tweet_input/tweets.txt"
output_dir = "tweet_output/ft2.txt"


graph = {}
hashtags_init = {}
output_data = []

with open(input_dir) as input_file:
    for line in input_file:
        tweet = json.loads(line)
        
        try:
            timestamp = int(tweet['timestamp_ms'])/1000
        
        except:
            continue
        
        try:
            hashtags = sp.unique(['#'+hashtag['text'].lower() for hashtag in tweet['entities']['hashtags']])
            # Cleaning
            hashtags = [hashtag.encode('ascii','ignore') for hashtag in hashtags]
            new_hashtags_init = dict([(hashtag, timestamp) for hashtag in hashtags])
        except:
            new_hashtags_init = {}
        
        expired_hashtags = [hashtag*((timestamp - hashtags_init.get(hashtag, timestamp)) > 60) for hashtag in hashtags_init.keys()]
        expired_hashtags =  filter(None, expired_hashtags)
        
        
        for hashtag in expired_hashtags:
            del hashtags_init[hashtag]
            graph = remove_edges(graph, hashtag)

        hashtags_init.update(new_hashtags_init)
        for hashtag in new_hashtags_init.keys():
            graph[hashtag] = list(sp.unique(graph.get(hashtag,[]) + new_hashtags_init.keys()))
            graph[hashtag].remove(hashtag)
        
        # Calculating
        degrees = [len(graph[node]) for node in graph.keys()]

        try:
            avg_degree = str(round(1.0*sum(degrees)/sp.count_nonzero(degrees),2))
        except:
            avg_degree = str(0)

        output_data.append(avg_degree)



with open(output_dir,'w') as output_file:
    output_file.write(os.linesep.join(output_data))

