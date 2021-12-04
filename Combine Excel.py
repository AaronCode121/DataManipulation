import pandas as pd
import glob
merged = []

def read(file):
    df = pd.read_excel(file, index_col=0)
    print(df.index.name)
    return df


xye_files = glob.glob('*.xlsx')
for var in xye_files:
    if xye_files.index(var) == 0:
        merged = read(var)
        unit = merged.index.name
    else:
        #merges two DataFrames where they overlap in x. Outer puts NaN where the data does not overlap
        merged = pd.merge(merged, read(var), on=[unit], how='outer')

# Sorts the x values into the correct order
merged = merged.sort_index()
merged.to_excel("combined data set.xlsx")