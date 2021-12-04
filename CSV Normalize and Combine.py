import pandas as pd
import glob
import matplotlib.pyplot as plt

# global variables
merged = []  # epmty DataFrame to place normalized values into
i = 0  # iteration counter

# extension of the file type to be converted to Excel
extension = '.csv' 

# normalization function 
def normalize(file):
    # import xye file
    df = pd.read_csv(file, index_col=0, names=['x', file,])

    # find min and max
    dfmin = df[file].min()
    dfmax = df[file].max()

    # normalize
    df[file] = (df[file] - dfmin) / (dfmax - dfmin)

    # remove old file type from name
    filename = file
    filename = filename.rstrip(extension)

    # export normalized data as CSV
    df.to_excel(filename+" normalized.xlsx")

    return df


# Search for all csv files and pass them to normalize
xye_files = glob.glob('*' + extension)

for var in xye_files:
    if xye_files.index(var) == 0:
        merged = normalize(var)
    else:
        # merges two DataFrames where they overlap in x. Outer puts NaN where the data does not overlap
        merged = pd.merge(merged, normalize(var), on=['x'], how='outer')

# Sorts the x values into the correct order
merged = merged.sort_index()

# exports the merged files to excel
merged.to_excel("combined normalization.xlsx")

