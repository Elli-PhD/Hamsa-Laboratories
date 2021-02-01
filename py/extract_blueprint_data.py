import yaml
import pandas as pd
import sys


exclude = ['activities']

file = open('blueprints.yaml','r')
##count = 0

x = []
while True:
##    count += 1
    
    # Get next line from file
    line = file.readline()
    
    # Check if line contains a string to exclude
    check = [ele for ele in exclude if(ele in line)]
    
    # if line is empty
    # end of file is reached
    if not line:
        break
    
    # if line does not include string to omit, add to list
    if len(check) == 0:
        x.append(line)
    else:
        pass

# convert list to dataframe
df = pd.DataFrame(x)

# generate a column name
df.columns = ['raw']
# remove unnecessary characters from dataframe
df['filtered'] = df['raw'].str.replace(':','')
df['filtered'] = df['filtered'].str.replace('\n','')
df['filtered'] = df['filtered'].str.replace(' ','')
df['filtered'] = df['filtered'].str.replace('-','')
print(df)


# establish variables to be used in conditionals
t1 = 0
t2 = 0
list_of_mat_quantity = []
list_of_mat_typeID = []
product_quantity = str()
product_typeID = str()
blueprintTypeID = str()
data = []

# scrub each line for useful data transform dataframe into more useful format
for i in df['filtered']:
    # first tier conditions: ignoring copying, invention, manufacturing, research_material, research_time
    if i in ['manufacturing']:
        t1 = 1
    elif i in ['copying', 'invention', 'research_material', 'research_time']:
        t1 = 0

    # second tier conditions: distinguishing between materials, products
    elif 'material' in i and t1 == 1:
        t2 = 1
    elif 'products' in i and t1 == 1:
        t2 = 2
    elif i in ['skills', 'time']:
        t2 = 0

    # third tier conditions: material and product quantities and typeIDs
    if 'quantity' in i and t1 == t2 == 1:
        list_of_mat_quantity.append(i)
    elif 'typeID' in i and t1 == t2 == 1:
        list_of_mat_typeID.append(i)
    elif 'quantity' in i and t1 == 1 and t2 == 2:
        product_quantity = i
    elif 'typeID' in i and t1 == 1 and t2 == 2:
        product_typeID = i

    # wrap up the loop and generate columns at the end of each item entry
    # corresponds to 'maxProductionLimit' entry
    elif 'blueprintTypeID' in i:
        blueprintTypeID = i
    elif 'maxProductionLimit' in i:
        # append data to list
        for j in range(len(list_of_mat_quantity)):
            data.append([blueprintTypeID, product_typeID, product_quantity, \
                        list_of_mat_typeID[j], list_of_mat_quantity[j]])        
        # reset variables
        list_of_mat_quantity = []
        list_of_mat_typeID = []
        product_quantity = str()
        product_typeID = str()
        blueprintTypeID = str()
        t1 = 0
        t2 = 0

# convert list to dataframe
data = pd.DataFrame(data)

# set columns
data.columns = ['Blueprint ID', 'Product ID', 'Product quanitity', 'Material ID', 'Material quantity']

# remove non-numerical data from dataframe
##data = data.replace(to_replace = ['blueprintTypeID*','typeID','quantity'], value = '')
for i in data.columns.to_list():
    data[i] = data[i].str.replace('blueprintTypeID','')
    data[i] = data[i].str.replace('typeID','')
    data[i] = data[i].str.replace('quantity','')
print(data[data['Blueprint ID'] == '17737'])





