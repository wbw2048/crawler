import json

import pandas as pd

df = pd.read_csv('/Users/wangbowen/Desktop/csv.csv')
for i, row in df.iterrows():
    print(row["camera_front_far"])
    print(row["camera_right_front"])
    print(json.loads(row["result"]))