'''
 Imports any data files with a defined extension (.csv by default) in the same folder as the script, merges the data along the same x values, 
 and exports an Excel file with combined data set     

 To work properly, all of the files in the folder with the specified extension should contain the same type of x values (wavelength, angles, lengths, counts)

 Although the data is merged along the x values, it is ok for the x values to start at different values (ie one file starting at x=0 and the other at x=4)

 File extension to be read, exportation of individial and or combined Excel files, normalization of the data and data plotting
 can all be toggled on or off in the global variables

 The lables for the x and y axis of any selected plots as well as the range for the x axis can be changed in the graphing variables
'''

# import libaries  
import pandas as pd
import glob
import matplotlib.pyplot as plt

# global variables

merged = []  # epmty DataFrame to place normalized values into
i = 0  # iteration counter

# extension to be searched for (commonly '.csv', '.tsv' or '.xye')
extension = '.csv' 

# turn functions on (True) or off (False)
export_individual = False  # export individual Excel files      
export_combined = True   # export Excel file containing all plots                      
normalize_data = True     # normalize the data
           
# graphing variables 
plot_graph = True #plot the data
stack = False # if True the plots will be stacked vertically (only works for normalized data)   
x_axis_label = 'x' # label for x axis
y_axis_label = 'y' # label for y axis
custom_x_axis = False # if True the minimun (start) and maximum (end) x values are set below
x_axis_start = 0 
x_axis_end = 0
  
# functions

# import data function, returns the contents of the file in the df DataFrame 
def read(file):
    
    # remove old file type from name
    filename = file
    filename = filename.rstrip(extension)

    # special treatment for .xye files
    if extension == ".xye":
        
        #specific step for .xye set and error column labeled
        df = pd.read_csv(file, sep='\s+', index_col=0, names=[x_axis_label, filename, 'Error'])
        
        # remove Error column
        df = df.drop(columns=['Error'])
    
    # normal import    
    else: df = pd.read_csv(file, index_col=0,names=[x_axis_label, filename])
    
    # removes y values of zero 
    df = df[(df != 0).all(1)]
    
    # normalization of data
    if normalize_data == True:
        df = normalize(df, filename)

    # export individual flie as .xlsx (Excel)
    if export_individual == True:
       
        # labels the file with normalized if that function was selected
        if normalize_data == True: 
            df.to_excel(filename + ' normalized.xlsx') 
        else: 
            df.to_excel(filename + '.xlsx') 

    return df

# normalization function, returns normalized data in the data DataFrame
def normalize(data, filename): 
    # find min and max
    datamin = data[filename].min()
    datamax = data[filename].max()

    # normalize formula
    data[filename] = (data[filename] - datamin) / (datamax - datamin)
        
    return data 

# graphing function
def graph(graph):
    graph.plot()
    plt.xlabel(x_axis_label)
    plt.ylabel(y_axis_label)
    plt.legend( loc='center', ncol=4, bbox_to_anchor=(0.5, 1.05), shadow=False, frameon=False)
    if custom_x_axis == True:
        plt.xlim(x_axis_start,x_axis_end)


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

# graphs the data
if plot_graph == True:
    graph(merged)
    if normalize_data == True & stack == True: # if stack was selected adds one to each normalized column stacking along the y axis
        for column in merged:
            merged[column] = merged[column] + i
            i = i + 1
        graph(merged)

# exports the merged files to Excel
if export_combined == True:
    
    # labels the Excel file with normalized if that function was selected
    if normalize_data == True:
        merged.to_excel("combined normalized data.xlsx") 
    else: 
        merged.to_excel("combined data set.xlsx")

#shows all graphs plotted
if plot_graph == True:
    plt.show()