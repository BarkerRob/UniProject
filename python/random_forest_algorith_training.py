import csv
import os

from python import random_forest_algorithm as rfa

path, dirs, files = next(os.walk('../algorithm results/random_forest/'))
file_count = len(files)
season = 2015 # Need to run for 2016

with open(f'../algorithm results/random_forest/random_forest_training_{season}_{file_count}.csv', 'w',
          newline='') as csv_file:
    algorithm_writer = csv.writer(csv_file, delimiter=',')
    algorithm_writer.writerow(['season', 'prediction', 'win', 'draw'])
    for i in range(1000):
        prediction, win, draw = rfa.main(season)
        algorithm_writer.writerow([season, prediction, win, draw])
