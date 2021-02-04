# Description

This set of python scripts is made for processing a csv file which contains tweets and generates a bubble like visualization of those tweets as a svg file.  The visualization displays tweets from oldest to most recent, the color of the nodes either represents the lang of the tweet or the number of times the tweet was retweeted (thanks to a red color gradient). 
The attributes_svg_insertion.py script 

## How to use it

STEPS :

1. Use the filtration_and_graph.py script

This script filters out retweets from tweets, agregates the followers of those retweeters onto the original tweets and it generates a swarmplot of the tweets as a gexf file. It also generates a new csv file later used to include attributes in the svg file. 
Two informations can be displayed in the node color :
 * The language of the tweets
 > python filtration_and_graph.py file.csv
 * The number of times the tweet was retweeted
 > python filtration_and_graph.py file.csv --nb_retweet

2 - Open the gexf file in Gephi, set the node size and run the noverlap algorithm

First set the node size using the total_flo attribute.
The spline for the node size might differ depending on the tweet distribution you have, this should be improved. 
Run the noverlap algorithm (speed : 1.1, ratio : 1.2,  margin : 0.02) 
Export the result as a svg file.

3 - Run the attributes_svg_insertion.py script

This script will add the following attributes to each node : author, text, sum_Rtfollower, lang, date of creation

> python attributes_svg_insertion.py file_filtered.csv file.svg 

