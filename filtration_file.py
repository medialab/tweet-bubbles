import csv


def processing_file(file,file1):
    with open(file) as f, open(file1,"w") as f2:
        file_content = csv.DictReader(f)
        headers = file_content.fieldnames
        headers.append("sum_Rtfollowers")
        writer = csv.DictWriter(f2, fieldnames = headers)
        writer.writeheader()
        tweets_o = []
        rt_o = []
        for row in file_content:
            if row["retweeted_id"]:
                rt_o.append(row)
            else:
                tweets_o.append(row)
        for tweet in tweets_o:
            S = int(tweet["from_user_followercount"])
            for rt in rt_o:
                if rt["retweeted_id"] == tweet["id"] and not(rt["from_user_id"] == tweet["from_user_id"]):
                    S += int(rt["from_user_followercount"])
            tweet.update({"sum_Rtfollowers":S})
            writer.writerow(tweet)

a = processing_file("/home/ptl7123/Bureau/finalisation_visu1/big_file.csv", "/home/ptl7123/Bureau/visu1_final/big_file_filtered.csv")
b = processing_file("/home/ptl7123/Bureau/finalisation_visu1/small_file.csv", "/home/ptl7123/Bureau/visu1_final/small_file_filtered.csv")


        
