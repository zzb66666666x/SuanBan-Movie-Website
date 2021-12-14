import csv
import os
import pandas as pd

profession_dict = {
    "miscellaneous": 0,
    "soundtrack": 1,
    "actor": 2,
    "actress": 3,
    "music_department": 4,
    "writer": 5,
    "director": 6,
    "producer": 7,
    "make_up_department": 8,
    "composer": 9,
    "assistant_director": 10,
    "camera_department": 11,
    "editor": 12,
    "cinematographer": 13,
    "casting_director": 14,
    "script_department": 15,
    "art_director": 16,
    "stunts": 17,
    "editorial_department": 18,
    "costume_department": 19,
    "animation_department": 20,
    "art_department": 21,
    "executive": 22,
    "special_effects": 23,
    "production_designer": 24,
    "production_manager": 25,
    "sound_department": 26,
    "talent_agent": 27,
    "casting_department": 28,
    "costume_designer": 29,
    "visual_effects": 30,
    "location_management": 31,
    "set_decorator": 32,
    "transportation_department": 33,
    "manager": 34,
    "legal": 35,
    "publicist": 36,
    "assistant": 37,
    "production_department": 38,
    "electrical_department": 39,
    "choreographer": 40
}

csv_table = pd.read_table(os.path.dirname(__file__)+"/name_basics.tsv", sep='\t')
csv_table.to_csv(os.path.dirname(__file__)+"/name_basics.csv", index=False)

with open(os.path.dirname(__file__)+"/name_basics.csv", 'rt') as csv_data:
    with open(os.path.dirname(__file__)+"/people.csv", "w") as csv_output_people:
        with open(os.path.dirname(__file__)+"/participate.csv", "w") as csv_output_participate:
            with open(os.path.dirname(__file__)+"/people_profession.csv", "w") as csv_output_profession:
                readers = csv.reader(csv_data, delimiter=',')
                writer_people = csv.writer(csv_output_people, delimiter=',')
                writer_participate = csv.writer(csv_output_participate, delimiter=',')
                writer_profession = csv.writer(csv_output_profession, delimiter=',')
                for line in readers:
                    if 'nconst' == line[0]:
                        continue
                    people_id = int(line[0][2:])
                    people_name = line[1]
                    if line[2].isdigit():
                        birth_year = int(line[2])
                    else:
                        birth_year = "\\N"
                    if line[3].isdigit():
                        death_year = int(line[3])
                    else:
                        death_year = "\\N"
                    people_description = "\\N"
                    writer_people.writerow([people_id, people_name, birth_year, death_year, people_description])
                    if '\\N' != line[4] and 0 != len(line[4]):
                        for profession in line[4].split(","):
                            profession_id = profession_dict[profession]
                            writer_profession.writerow([people_id, profession_id])
                    if '\\N' != line[5]:
                        for video in line[5].split(","):
                            video_id = int(video[2:])
                            writer_participate.writerow([video_id, people_id, "\\N"])
