import csv
import os

with open(os.path.dirname(__file__)+"/user.csv", "w") as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for i in range(4, 1024):
        writer.writerow([i, "Demo User " + str(i), "demo_user_" + str(i) + "@demo", "false", "Demo_411_" + str(i), "false", "Demo User " + str(i)])
