import csv
import networkx as nx 
from tqdm import tqdm
import math
from collections import Counter
import argparse 
from numpy import arange

#compter le nombre de langues

TAILLE_MAX = 100
G = nx.Graph()
couleur = {"en" : [199,102,116], "fr" : [105,126,213], "und" : [154,153,69], "es": [147,80,161]}
#couleur = {"fr" : [101,136,202], "en": [212,66,86], "und" : [179,151,64], "es" : [203,100,45], "pt" :[107,166,71], "others" : [155,75,128]}
### taking inline command 

parser = argparse.ArgumentParser(description='Filter a csv file and generate a gexf graph')
parser.add_argument('filename')
parser.add_argument("--gradient", help="add a gradient of color to the node distribution (from black to red)")
args = parser.parse_args()

#### generating a new csv file ? 

file1 = args.filename[:-4]  + "_filtered2.csv"
graphe = args.filename[:-4] + "graphe.gexf"



### filtering and writing a new csv file #### 
with open(args.filename) as f, open(file1,"w") as f2:
    file_content = csv.DictReader(f)
    headers = file_content.fieldnames
    headers.append("sum_Rtfollowers")
    writer = csv.DictWriter(f2, fieldnames = headers)
    writer.writeheader() 
    tweets_o1 = dict()
    tweets_o2 = Counter()
    rt_o = []
    for row in file_content:
        if row["retweeted_id"]:
            rt_o.append(row)
        else:
            tweets_o1.update({"{}".format(row["id"]) : row})
            tweets_o2[row["id"]] = int(row["from_user_followercount"])
    for rt in rt_o:
        # rt["from_user_id"] has loads of chance not to be a key of tweets_o1 hence the try block
        try:
            if not(rt["from_user_id"] == tweets_o1[rt["retweeted_id"]]["from_user_id"]):
                tweets_o2[rt["retweeted_id"]] += int(rt["from_user_followercount"])
        except:
            pass
    for x in tweets_o1:
        tweets_o1[x].update({"sum_Rtfollowers":tweets_o2[x]})
        writer.writerow(tweets_o1[x])


### we store the content of file1 in RAM as we are going to consume the file three times. 
file_content = []
with open(file1) as f:
    file_c = csv.DictReader(f)
    for row in file_c:
        file_content.append(row)

"""def get_stats_file(fichier1):
    This function allows us to get a suitable time pace which will be used later on when 
    drawing the graph"""
n = 0 
maxi_time = - math.inf
mini_time = math.inf
maxi_size = - math.inf
mini_size = math.inf

for row in file_content:
    n +=1
    if float(row["time"])> maxi_time:
        maxi_time = float(row["time"])
    if float(row["time"])< mini_time:
        mini_time = float(row["time"])
    if float(row["sum_Rtfollowers"])> maxi_size:
        maxi_size = float(row["sum_Rtfollowers"])
    if float(row["sum_Rtfollowers"])< mini_size:
        mini_size = float(row["sum_Rtfollowers"])
  

pace = (maxi_time - mini_time)/n * 0.9
t = mini_time - 0.1*pace

"""Creating a first dictionnary which keys are the time distribution previously defined. The values are 
coordinates"""

time_partitions= dict() 
Y = 4000

while t < maxi_time:
    time_partitions.update({t : [Y,0]})
    Y -= 10
    t += pace
time_partitions.update({(t-pace)+0.01*pace: [Y,0]})


time_part = dict()
Z = 4000


### We stock the content of the file in a list so we do not have to open the file1 twice

### Filtrating no point's land  
a = 0
d = Counter()
for row in file_content:
    tem = float(row["time"])
    for x in time_partitions.keys():
        if not (tem > x and tem < x + pace):
            continue
        d[x] += 1
# This c variable will be used to make a color gradient in order to see if the noverlap algo works fine
c = 0
for x in time_partitions.keys():
    #We only keep intervals that actually contains tweets
    if x in d:
        if c < 200:
            c = c + 5
        time_part.update({x :[Z,0,c]})
        Z -= 15

#with open(file1) as f:
   # file_content = csv.DictReader(f)
for row in file_content:
    tweet_id = row["id"]
    author = row["from_user_name"]
    lg = row["lang"]
    text_tweet = row["text"]
    total_followers = row["sum_Rtfollowers"]
    G.add_node(tweet_id, author = author, text_tweet = text_tweet) #, author = author, text = text_tweet, nb_of_followers = total_followers)
    if float(total_followers)==mini_size:
        G.nodes[tweet_id]["viz"] = {"size" : math.log(TAILLE_MAX*(float(maxi_size) + 1) /float(maxi_size))*0.18} #TAILLE_MAX*math.log((float(total_followers))))/math.log(float(maxi_size)
    else:
        G.nodes[tweet_id]["viz"] = {"size" : math.log(TAILLE_MAX*(float(total_followers) + 1) /float(maxi_size)) }
    tem = float(row["time"])
    c = 0
    for x in time_part.keys():
        # For usual cases, we check whether the time of the tweet is in the current time interval
        if not (tem > x and tem < x + pace):
            continue
        if args.gradient:
            G.nodes[tweet_id]["viz"]["color"] = {"r": int(time_part[x][2]) , "g": 0 ,"b" : 0, "a" : 1.0}
        else:
            try:
                G.nodes[tweet_id]["viz"]["color"] = {"r": couleur[lg][0] , "g": couleur[lg][1] ,"b" : couleur[lg][2], "a" : 1.0}
            except:
                G.nodes[tweet_id]["viz"]["color"] = {"r": couleur["others"][0] , "g": couleur["others"][1] ,"b" : couleur["others"][2], "a" : 1.0}
            #small_file 4 un : 154,153,69, fr : 105,126,213, en : 199,102,116, es : 147,80,161
        position = time_part[x][1]
        hauteur = time_part[x][0]
        pas = 15
            # Here we distribute tweets that are in the same time bin on the x axis 
        if position == 0:
            G.nodes[tweet_id]["viz"]["position"] = {"x": 0, "y": float(hauteur), "z" : 0.0} 
        elif position == 1:
            G.nodes[tweet_id]["viz"]["position"] = {"x": pas, "y": float(hauteur), "z" : 0.0} 
        elif position % 2 == 0:
            G.nodes[tweet_id]["viz"]["position"] = {"x": -float((position//2)*pas), "y": float(hauteur), "z" : 0.0} 
        else: 
            G.nodes[tweet_id]["viz"]["position"] = {"x": float((position//2)*pas) + pas, "y": float(hauteur), "z" : 0.0}
        time_part[x][1] += 1

nx.write_gexf(G, graphe)
