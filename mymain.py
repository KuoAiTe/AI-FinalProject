'''Balanced clustering of online retail orders'''
import csv
import numpy as np
from kmodes.kmodes import KModes

csvFile = open("new.csv", "r")
reader = csv.reader(csvFile)
    
result = {}
i = 0
for row in reader:
    # if reader.line_num == 1:
    #     continue
    if reader.line_num >= 10:
        break
    print(row)

csvFile.close()
# print(result)

# framework
# Sampling


# K-means clustering


# Populating and Refining


