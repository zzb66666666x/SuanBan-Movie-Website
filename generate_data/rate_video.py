import csv
import os
import numpy as np
import pandas as pd
import datetime

csv_table = pd.read_table(os.path.dirname(__file__)+"/title_ratings.tsv", sep='\t')
csv_table.to_csv(os.path.dirname(__file__)+"/title_ratings.csv", index=False)

with open(os.path.dirname(__file__)+"/title_ratings.csv", 'rt') as csv_data:
    with open(os.path.dirname(__file__)+"/rate_video.csv", "w") as csv_output:
        readers = csv.reader(csv_data, delimiter=',')
        writer = csv.writer(csv_output, delimiter=',')
        for line in readers:
            if 'tconst' == line[0]:
                continue
            video_id = int(line[0][2:])
            average_rating = float(line[1])
            gaussian_scale = min(10 - average_rating, average_rating - 1) / 3
            num_votes = min(16, int(line[2]))
            user_id_list = np.random.randint(4, 1024, num_votes)
            rate_list = np.random.normal(average_rating, gaussian_scale, num_votes)
            for i in range(num_votes):
                rate = rate_list[i]
                while 0.5 >= rate or 10.5 < rate:
                    rate = np.random.normal(average_rating, gaussian_scale)
                writer.writerow([video_id, user_id_list[i], round(rate), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
