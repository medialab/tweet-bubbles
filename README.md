# Description

This set of python scripts is made for processing a csv file which contain tweets, those scripts filter out tweets that are not retweeted and agregate the sum of the followers 

## How to use it


### 1 - Use the filtration_and_graph.py script
 This Script will generate a filtered csv file and a gexf file. In the command line you need to indicate the path to your tweet csv file. A color gradient can be add (the color is fixed : red)
 by adding the option : --gradient  to the commandline

### 2 - Open the gexf file in Gephi and run the Noverlap algorithm 

parameters : (speed : 1.1, ratio : 1.2, margin = 0.02) 
export to svg format

#### 3 - Use the attributes_svg_insertion.py script

This script will add the following attributes to each node : author, text, sum_Rtfollower
You need to specify in the commandline in this order : the csv file, the SVG file



