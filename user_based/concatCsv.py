import pandas as pd
import glob

all_files = glob.glob("./dataNotesFromUsers*.csv")

li = []
print(all_files)
for filename in all_files:
    df = pd.read_csv(filename, error_bad_lines=False)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)
# frame = frame[frame['contributionNbr'].str.len() > 1]
frame.to_csv('mergeDataNotesFromUsers.csv', index=False)