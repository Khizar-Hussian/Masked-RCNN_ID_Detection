import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from ast import literal_eval
import json

ANNOTATION_PATH = "./annotation files/UK_DL_annotations_csv.csv"
LABELS_PATH = "./uk_dv_labels/"

# check if direcotries exist, if not create them
if not os.path.exists(LABELS_PATH):
    os.mkdir(path=LABELS_PATH)
    print(f"{LABELS_PATH} created.")


def read_annotations(path):
    df = pd.read_csv(path)
    df['region_attributes'] = df['region_attributes'].apply(literal_eval)
    df['region_shape_attributes'] = df['region_shape_attributes'].apply(literal_eval)
    return df

def get_XYWH(row):
    x = row['region_shape_attributes']['x']
    y = row['region_shape_attributes']['y']
    w = row['region_shape_attributes']['width']
    h = row['region_shape_attributes']['height']
    return x,y,w,h

def get_points(row):
    X = row['region_shape_attributes']['all_points_x']
    Y = row['region_shape_attributes']['all_points_y']
    x1 =(X[0], Y[0])
    x2 =(X[1], Y[1])
    x3 =(X[2], Y[2])
    x4 =(X[3], Y[3])
    return (x1, x2, x3, x4)

def main():
    df = read_annotations(ANNOTATION_PATH)
    print("[+] Annotations loaded")
    for i in range(0, len(df), 6):
        data = {}
        rows = df.iloc[i:i+6, :]
        filename = rows.iloc[0, :]['filename'].split('.')[0]
        try:
            data['name'] =  get_points(rows.iloc[0, :])
            data['dob'] =   get_points(rows.iloc[1, :])
            data['isd'] =   get_points(rows.iloc[2, :])
            data['exd'] =   get_points(rows.iloc[3, :])
            data['lno'] =   get_points(rows.iloc[4, :])
            data['add'] =   get_points(rows.iloc[5, :])

            with open(os.path.join(LABELS_PATH, f"{filename}.json"), 'w') as outfile:
                json.dump(data, outfile)
        except Exception as e:
            print(e)
            print(filename)

    print("[+] Completed label file creation.")


if __name__ == "__main__":
    main()
