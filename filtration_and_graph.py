import csv
import networkx as nx
from tqdm import tqdm
import math
from collections import Counter
import argparse
import os
from seaborn import color_palette

parser = argparse.ArgumentParser(description='Filter a csv file and generate a gexf graph')
parser.add_argument('filename')
parser.add_argument("--nb_retweet", help="add a gradient of color to the node distribution (from black to red), the redder the tweet is the more it has been rt", action = 'store_true')
args = parser.parse_args()

graphe = os.path.splitext(args.filename)[0] + "_graphe.gexf"
file1 = os.path.splitext(args.filename)[0] + "_filtered.csv"


def get_data(csv_file):
    """
    Function that retrieves data from twitter (gazouilloire) file.

    input :
        gazouilloire csv file

    output:
        tweets_o1(dict) contains tweets that are not rts. keys : tweetid, values : row
        tweets_o2(dict) key : tweet_id, value : number of followers
        rt_o(list) contains tweets that are rt
        langs(Counter) key : lang, value : number of tweets in that language
    """
    tweets_o1 = dict()
    tweets_o2 = dict()
    rt_o = []
    langs = Counter()
    with open(csv_file) as f:
        file_content = csv.DictReader(f)
        for row in tqdm(file_content):
            if row["retweeted_id"]:
                rt_o.append(row)
            else:
                tweets_o1[row["id"]] = row
                tweets_o2[row["id"]] = {'followers': int(row["from_user_followercount"]), 'nb':0}
                langs[row['lang']] += 1
    return (tweets_o1, tweets_o2, rt_o, langs)

def gen_color(l_lang):
    """
    function that generates a color palette for the most 5 popular lang in the corpus

    input:
        l_lang(Counter) keys: language, values: number of tweets in that language

    output:
        couleur(dict) keys: language, values : RGB values
    """
    couleur = dict()
    langs = l_lang.most_common()[0:5]
    colors = [(int(255*x[0]),int(255*x[1]),int(255*x[2])) for x in color_palette('hls',len(langs)+1)]
    couleur['other'] = colors.pop()
    for lang in langs:
        couleur[lang[0]] = colors.pop()
    return couleur

def agregate_followers(tweets_o1, tweets_o2, rt_o):
    """
    This functions agregates followers from retweeters on the 'primary' tweet.
    It also count the number of retweets for a specific tweet
    """
    for rt in rt_o:
        val = tweets_o1.get(rt['retweeted_id'],None)
        if val:
            val = val.get("from_user_id")
        if val and not(rt["from_user_id"] == val):
            tweets_o2[rt["retweeted_id"]]["followers"] += int(rt["from_user_followercount"])
            tweets_o2[rt["retweeted_id"]]["nb"] += 1
        else:
            pass
    for x in tweets_o1:
        tweets_o1[x]["sum_Rtfollowers"] = tweets_o2[x]['followers']
        tweets_o1[x]["nb_rt"] = tweets_o2[x]['nb']

def write_filt_file(file2, tweets_o1):
    headers = list(tweets_o1[list(tweets_o1.keys())[0]].keys())
    with open(file2,'w') as f2:
        writer = csv.DictWriter(f2, fieldnames = headers)
        writer.writeheader()
        for row in tweets_o1:
            writer.writerow(tweets_o1[row])


def getMinsMax(tweets_o1):
    """
    Returns useful informations about the tweet distribution: 
        - maxi_size (float) Number of maximum followers (agregated on a single tweet)
        - mini_size (float) Number of minimum followers (agregated on a single tweet)
        - mini_time (float) lowest time of the tweet distribution
        - maxi_time (float) upper time of the tweet distribution
        - count_rt (Counter) key : number of retweets of the tweet , value : number of tweets that have been retweeted key amount of time
    """
    n = 0
    maxi_time = - math.inf
    mini_time = math.inf
    maxi_size = - math.inf
    mini_size = math.inf
    max_rt = -math.inf
    count_rt = Counter()
    for row in tqdm(tweets_o1.values()):
        n +=1
        if float(row["time"])> maxi_time:
            maxi_time = float(row["time"])
        if float(row["time"])< mini_time:
            mini_time = float(row["time"])
        if float(row["sum_Rtfollowers"])> maxi_size:
            maxi_size = float(row["sum_Rtfollowers"])
        if float(row["sum_Rtfollowers"])< mini_size:
            mini_size = float(row["sum_Rtfollowers"])
        if float(row["nb_rt"])> max_rt:
            max_rt = float(row["nb_rt"])
        count_rt[row["nb_rt"]] += 1
    return [{'max_time': maxi_time, 'min_time': mini_time, 'max_followers': maxi_size, 'min_followers': mini_size, 'max_rt': max_rt, 'tt_row' : n}, count_rt]

def get_classes_grad(count_rt):
    '''
    Function used to apply a gradient of red color () if the arg --nb_retweet is passed
    '''
    stat = sorted(count_rt.items()) #ordered nb of rt items. list of tuples
    ordered_rts_col = []
    cl = []
    cumul_rt = 0 # nb of tweets that have been retweeted 0,1...,totalrts
    total_number_rts = 0
    for nb_rt in count_rt:
        total_number_rts += count_rt[nb_rt] # total len of rts
    color = 0
    quartile = (total_number_rts+3)/4
    for rt in stat:
        cumul_rt += rt[1]
        tato = list(rt)
        tato.append(64) # 64*4 = 256
        cl.append(tato)
        if cumul_rt >= quartile:
            ordered_rts_col.append(cl)
            quartile += (total_number_rts-1)/4
            cl = []
    if cl:
        ordered_rts_col.append(cl)
    color = 0
    final_rts_color = dict()
    for rts in ordered_rts_col:
        for element in rts:
            color += element[2]/len(rts)
            final_rts_color[element[0]] = [element[1],color]
    return final_rts_color

def create_bin_timestamp(max_time, min_time,n, tweets_o1):
    '''
    This function creates a timestamp later used to ordonate the tweets
    '''
    pace = (maxi_time - min_time)/n * 0.9
    t = min_time - 0.1*pace
    time_partitions= dict()
    height1 = 4000
    while t < maxi_time:
        time_partitions[t] = [height1,0]
        height1 -= 10
        t += pace
    time_partitions[(t-pace)+0.01*pace] = [height1,0]
    #No man's land : We only keep intervals that actually contains tweets
    temps_ecreme = set()
    for row in tqdm(tweets_o1.values()):
        tem = float(row["time"])
        for time in time_partitions.keys():
            if not (tem > time and tem < time + pace):
                continue
            temps_ecreme.add(time)
    time_part = dict()
    height2 = 4000
    for time in tqdm(time_partitions.keys()):
        if time in temps_ecreme:
            time_part[time] =[height2,0]
            height2 -= 10
    return time_part,pace

def write_graph(tweets_o1,time_part,pace,langs,nb_rt = False):
    """
    Function that generates a gexf file swarmplot like
    """
    G = nx.Graph()
    couleur = gen_color(langs)
    for row in tqdm(tweets_o1.values()):
        tweet_id = row["id"]
        author = row["from_user_name"]
        lg = row["lang"]
        text_tweet = row["text"]
        total_followers = row["sum_Rtfollowers"]
        rt = row['nb_rt']
        tem = float(row["time"])
        G.add_node(tweet_id, author = author, text_tweet = text_tweet, total_flo = total_followers)
        G.nodes[tweet_id]["viz"] = {"size" : 1 } #init
        if nb_rt:
            G.nodes[tweet_id]["viz"]["color"] = {"r": int(classes2[rt][1]) , "g": 0 ,"b" : 0, "a" : 1.0}
        else:
            col = couleur.get(lg, couleur["other"])
            G.nodes[tweet_id]["viz"]["color"] = {"r": col[0] , "g": col[1] ,"b" : col[2], "a" : 1.0}
        for x in time_part.keys():
            # For usual cases, we check whether the time of the tweet is in the current time interval
            if not (tem > x and tem < x + pace):
                continue
            position = time_part[x][1]
            hauteur = time_part[x][0]
            pas = 10
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


if __name__ == '__main__':
    tweets_o1, tweets_o2, rt_o, langs = get_data(args.filename)
    agregate_followers(tweets_o1,tweets_o2,rt_o)
    #print(list(tweets_o1[list(tweets_o1.keys())[0]].keys()))
    write_filt_file(file1,tweets_o1)
    Maxs, count_rt =  getMinsMax(tweets_o1)
    classes2 = get_classes_grad(count_rt)
    maxi_time = Maxs['max_time']
    min_time = Maxs['min_time']
    maxi_size = Maxs['max_followers']
    mini_size = Maxs['min_followers']
    n = Maxs['tt_row']
    time_p, pace = create_bin_timestamp(maxi_time, min_time,n,tweets_o1)
    if args.nb_retweet:
        write_graph(tweets_o1,time_p,pace,langs,nb_rt=True)
    else:
        write_graph(tweets_o1,time_p,pace,langs )
