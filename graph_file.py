import csv
import networkx as nx 
from tqdm import tqdm
from math import sqrt, log
from collections import Counter

def generate_graph(fichier, fichier2):
    def get_bin_time(fichier1):
        """ This function allows us to get a suitable time pace which will be used later on when 
        drawing the graph"""
        n = 0 
        maxi = 0.0
        mini = 90000000000000
        with open(fichier1, "r+") as f1:
            file_content = csv.DictReader(f1)
            for row in file_content:
                n +=1
                if float(row["time"])> maxi:
                    maxi = float(row["time"])
                if float(row["time"])< mini:
                    mini = float(row["time"])
            return ((maxi - mini)/n, mini, maxi, n)  

    tempo = get_bin_time(fichier)
    Total_time = tempo[2]
    pace = tempo[0]*0.9

    t = tempo[1] - 0.1*pace

    def get_stats_followers(fichier1):
        """ This function return the min and the max of the Sum_Rtfollowers field """
        mini = 99
        maxi = 0
        with open(fichier1, "r+") as f1:
            file_content = csv.DictReader(f1)
            for row in file_content:
                if float(row["sum_Rtfollowers"])> maxi:
                    maxi = float(row["sum_Rtfollowers"])
                if float(row["sum_Rtfollowers"])< mini:
                    mini = float(row["sum_Rtfollowers"])
        return (mini, maxi)  

    stats = get_stats_followers(fichier)
    mini = stats[0]
    maxi = stats[1]

    taille_max = 100


    """Creating a first dictionnary which keys are the time distribution previously defined. The values are 
    coordinates"""
    time_partitions = dict() 
    Y = 4000
    while t < Total_time:
        time_partitions.update({t : [Y,0]})
        Y -= 100
        t += pace
    time_partitions.update({(t-pace)+0.01*pace: [Y,0]})
    G = nx.DiGraph()
    time_part = dict()
    Z = 4000

    ### Filtrating no point land  
    with open(fichier) as f:
        file_content = csv.DictReader(f)
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
                Z -= 30

    with open(fichier) as f:
        file_content = csv.DictReader(f)
        for row in file_content:
            tweet_id = row["id"]
            author = row["from_user_name"]
            text_tweet = row["text"]
            total_followers = row["sum_Rtfollowers"]
            G.add_node(tweet_id, author = author, text_tweet = text_tweet) #, author = author, text = text_tweet, nb_of_followers = total_followers)
            G.nodes[tweet_id]["viz"] = {"size" : (taille_max*log((float(total_followers) +1)))/log(float(maxi))} 
            tem = float(row["time"])
            c = 0
            for x in time_part.keys():
                # For usual cases, we check whether the time of the tweet is in the current time interval
                if not (tem > x and tem < x + pace):
                    continue
                G.nodes[tweet_id]["viz"]["color"] = {"r": int(time_part[x][2]) , "g": 0 ,"b" : 0, "a" : 1.0}
                position = time_part[x][1]
                hauteur = time_part[x][0]
                pas = 70
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

    nx.write_gexf(G, fichier2)


generate_graph("/home/ptl7123/Bureau/visu1_final/big_file_filtered.csv","grand_graphe.gexf")
generate_graph("/home/ptl7123/Bureau/visu1_final/small_file_filtered.csv","petit_graphe.gexf")