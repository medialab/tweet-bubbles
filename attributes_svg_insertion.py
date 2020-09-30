import csv
from bs4 import BeautifulSoup
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('graphe')
args = parser.parse_args()

graphe2 = args.graphe[:-5]  + "3.svg"

with open(args.filename) as f1, open(args.graphe) as f2, open(graphe2, "w") as f3:
        file_content = csv.DictReader(f1)
        soup = BeautifulSoup(f2,'xml')
        nodes = soup.g
        circles = nodes.select('circle')
        for row in file_content:
            for circle in circles:
                if row["id"] == circle["class"][3:]:
                    author = row["from_user_name"]
                    text = row["text"]
                    sum_followers = row["sum_Rtfollowers"]
                    title = soup.new_tag("title")
                    title.insert(1, "author : {}, text = {}, agregation du nombre de followers sur le tweet : {}".format(author,text,sum_followers))
                    circle.append(title)
                    circle["author"] = author
                    circle["text"] = text
                    circle["sum_Rtfollowers"] = row["sum_Rtfollowers"]
                    circle["lang"] = row["lang"]
                    circle["date"] = row["created_at"]
        f3.write(str(soup))

