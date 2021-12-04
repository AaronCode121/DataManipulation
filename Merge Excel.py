# script to merge excel files into a single file called combined data set
# all files must have labels in the top row and have the same label for the independant variable
import pandas as pd
import glob

# global variables
merged = []  # epmty DataFrame to place normalized values into
i = 0  # iteration counter

# custom variables
extension = '.xlsx'  # Excel file extension
ind_var = 'x' # the lable of the independant variable in all Excel files to be merged               

# import data function 
def read(file):
    
    # remove file type from name
    filename = file
    filename = filename.rstrip(extension) 

    # import excel file, header=0 sets the first column as the df names 
    df = pd.read_excel(file, index_col=0, header=0) 

    return df

# search for all files with specified extension
files = glob.glob('*' + extension)

for var in files: # itterates through all the file found in the search
    if files.index(var) == 0:
        merged = read(var) #inputs the first file into the merged DataFrame
    else:
        # merges two DataFrames. Values are merged on the specified indipendant variable  
        # outer puts NaN where the data does not overlap
        merged = pd.merge(merged, read(var), on=ind_var, how='outer')

# exports the merged excel file
merged.to_excel("combined data set.xlsx")
