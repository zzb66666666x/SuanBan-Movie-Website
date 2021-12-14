import csv
import os
import numpy as np
import datetime

with open(os.path.dirname(__file__)+"/people.csv", 'rt') as csv_data:
    with open(os.path.dirname(__file__)+"/rate_people.csv", "w") as csv_output:
        readers = csv.reader(csv_data, delimiter=',')
        writer = csv.writer(csv_output, delimiter=',')
        counter = 0
        for line in readers:
            if 128 < counter:
                break
            counter += 1
            people_id = int(line[0])
            average_rating = 6
            gaussian_scale = min(10 - average_rating, average_rating - 1) / 3
            num_votes = 3
            user_id_list = np.random.randint(4, 1024, num_votes)
            rate_list = np.random.normal(average_rating, gaussian_scale, num_votes)
            for i in range(num_votes):
                rate = rate_list[i]
                while 0.5 >= rate or 10.5 < rate:
                    rate = np.random.normal(average_rating, gaussian_scale)
                writer.writerow([people_id, user_id_list[i], round(rate), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
