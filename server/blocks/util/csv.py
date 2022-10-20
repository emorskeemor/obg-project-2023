import csv
import os

def read_csv(path) -> list: 
    if not os.path.exists(path):
        return None   
    with open(path, "r") as f:
        reader = csv.reader(f, delimiter=",")
        return list(reader)
    