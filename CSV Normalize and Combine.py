'''
 Imports any data files with a defined extension (.csv by default) in the same folder as the script, merges the data along the same x values, 
 and exports an Excel file with combined data set     

 To work properly, all of the files in the folder with the specified extension should contain the same type of x values (wavelength, angles, lengths, counts)

 Although the data is merged along the x values, it is ok for the x values to start at different values (ie one file starting at x=0 and the other at x=4)

'''

# import libaries  
import pandas as pd
import glob
import matplotlib.pyplot as plt

# global variables

merged = []  # epmty DataFrame to place normalized values into
i = 0  # iteration counter
x = "" # data label

# extension to be searched for (commonly '.csv', '.tsv' or '.xye')
extension = '.csv' 
             
# functions

# import data function, returns the contents of the file in the df DataFrame 
def read(file):
    
    # remove old file type from name
    filename = file
    filename = filename.rstrip(extension)

    # special treatment for .xye files
    if extension == ".xye":
        
        #specific step for .xye set and error column labeled
        df = pd.read_csv(file, sep='\s+', index_col=0, names=[x, filename, 'Error'])
        
        # remove Error column
        df = df.drop(columns=['Error'])
    
    # normal import    
    else: df = pd.read_csv(file, index_col=0,names=[x, filename])
    
    # removes y values of zero 
    df = df[(df != 0).all(1)]
    
    # normalization of data
    df = normalize(df, filename)

    return df

# normalization function, returns normalized data in the data DataFrame
def normalize(data, filename): 
    # find min and max
    datamin = data[filename].min()
    datamax = data[filename].max()

    # normalize formula
    data[filename] = (data[filename] - datamin) / (datamax - datamin)
        
    return data 


# start of script  

# search for all files with specified extension and pass them to the normalize function
search_files = glob.glob('*' + extension)


for var in search_files: #iterates through all the file found in the search
    if search_files.index(var) == 0:
        merged = read(var) #inputs the first file into the merged DataFrame
    else:
        # merges two DataFrames where they overlap in x. Outer puts NaN where the data does not overlap
        merged = pd.merge(merged, read(var), on=[x_axis_label], how='outer')

# sorts the x values into the correct order
merged = merged.sort_index()

# exports the combined normalized data in an Excel file
merged.to_excel("combined normalized data.xlsx") 