import glob
import csv
import json
import os
import pandas as pd

files = glob.glob('/home/app/Desktop/output_china//**//Background.csv', recursive = True)
count = 0


df = pd.DataFrame(columns=['manager', 'manager_link'])


#print(fnames)
for f in files[:39155:]:
    with open(f) as csv_file:
        data = pd.read_csv(csv_file)
        if data['基金管理人'].iloc[0] in df['manager']:
            pass
        else:
            df.loc[count]  = [data['基金管理人'].iloc[0], '']
    count = count+1


df.to_csv('manager.csv')

print (df)
