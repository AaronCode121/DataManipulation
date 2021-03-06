'''
 Script to merge all Excel files in the same folder as the script into a single Excel file

 All Excel files must have labels in the top row and have the same label for the independant (x) variable. The lable for the independant variable 
 must be entered in ind_var variable under global variables
'''
# import libaries 
import pandas as pd
import glob

# global variables
merged = []  # epmty DataFrame to place normalized values into
i = 0  # iteration counter

# custom variables
extension = '.xlsx'  # Excel file extension, can be set to .xls for older excel files
ind_var = 'x' # the lable of the independant variable in all Excel files to be merged               

# import data function, returns the contents of the file in the df DataFrame 
def read(file):
    
    # remove file type from name
    filename = file
    filename = filename.rstrip(extension) 

    # import excel file, header=0 sets the first column as the df names 
    df = pd.read_excel(file, index_col=0, header=0) 

    return df

# search for all files with specified extension
files = glob.glob('*' + extension)

for var in files: # iterates through all the file found in the search
    if files.index(var) == 0:
        merged = read(var) #inputs the first file into the merged DataFrame
    else:
        # merges two DataFrames. Values are merged on the specified indipendant variable  
        # outer puts NaN where the data does not overlap
        merged = pd.merge(merged, read(var), on=ind_var, how='outer')

# exports the merged Excel file
merged.to_excel("combined data set.xlsx")
