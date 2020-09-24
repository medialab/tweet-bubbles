# Description

This set of python scripts is made for processing a csv file which contain tweets, those scripts filter out tweets that are not retweeted and agregate the sum of the followers 

## How to use it

1 - Create a folder, Put your twitter csv file in it and create an other blank csv file.

2 - line 26-27 of filtration_file.py, remplace the first processing arg by your twitter csv file

3 - run filtration_file.py

4 - Change line 117-118 of graph_file.py delete, add lines and change first arg of generate_graph

5 - Open the gexf file on Gephi, use the noverlap algo with (speed : 1.1, ratio : 1.2, margin = 0.02) and export to svg format

6 - Run attributes_svg_insertion.py (change line 22, 23 according to the name of your files)


