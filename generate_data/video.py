import csv
import os
import pandas as pd

category = {
    "movie": 0,
    "short": 1,
    "tvEpisode": 2,
    "tvMiniSeries": 3,
    "tvMovie": 4,
    "tvSeries": 5,
    "tvSpecial": 6,
    "video": 7,
    "tvShort": 8,
    "videoGame": 9,
    "radioEpisode": 10,
    "tvPilot": 11
}

csv_table = pd.read_table(os.path.dirname(__file__)+"/title_basics.tsv", sep='\t')
csv_table.to_csv(os.path.dirname(__file__)+"/title_basics.csv", index=False)

with open(os.path.dirname(__file__)+"/title_basics.csv", 'rt') as csv_data:
    with open(os.path.dirname(__file__)+"/video.csv", "w") as csv_output:
        readers = csv.reader(csv_data, delimiter=',')
        writer = csv.writer(csv_output, delimiter=',')
        for line in readers:
            if 'tconst' == line[0]:
                continue
            video_id = int(line[0][2:])
            video_name = line[2]
            original_name = line[3]
            video_description = line[8]
            if line[5].isdigit():
                start_year = int(line[5])
            else:
                start_year = "\\N"
            if line[6].isdigit():
                end_year = int(line[6])
            else:
                end_year = "\\N"
            if line[7].isdigit():
                runtime_minutes = int(line[7])
            else:
                runtime_minutes = "\\N"
            category_id = category[line[1]]
            writer.writerow([video_id, video_name, original_name, video_description, start_year, end_year, runtime_minutes, category_id])
