import csv
from bs4 import BeautifulSoup


def attribut(fichiercsv, graphe1, graphe2):
    with open(fichiercsv) as f1, open(graphe1, "r+") as f2, open(graphe2, "w") as f3:
        file_content = csv.DictReader(f1)
        soup = BeautifulSoup(f2,'xml')
        nodes = soup.g
        good_nodes = []
        for node in nodes:
            if type(node)==type(nodes):
                good_nodes.append(node)
        for row in file_content:
            for node in good_nodes:
                if row["id"] == node["class"][3:]:
                    node["author"] = row["from_user_name"]
                    node["text"] = row["text"]
                    node["sum_Rtfollowers"] = row["sum_Rtfollowers"]
        f3.write(str(soup))

attribut("/home/ptl7123/Bureau/visu1_final/big_file_filtered.csv", "grand_graphe.svg", "grand_graphe2.svg")
attribut("/home/ptl7123/Bureau/visu1_final/small_file_filtered.csv", "petit_graphe.svg", "petit_graphe2.svg")