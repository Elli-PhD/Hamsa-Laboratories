import yaml
import pandas as pd
import sys

""" A function to read YAML file """
def read_yaml(filename):
    with open('%s'%filename, encoding='utf-8') as f:
        file = yaml.load(f, Loader=yaml.FullLoader)
##        file = yaml.safe_load(f)
    return file

""" Load blueprints.yaml and convert 'product' and 'materials' data to JMP table """

print('Loading blueprints.yaml...')
blueprints = read_yaml('blueprints.yaml')
print('Completed loading blueprints.yaml\n\n')

##df = []
##for i in blueprints:
##    try:
##        entry = blueprints[i]
##        m_data = entry['activities']['manufacturing']
##        m_data = {key: m_data[key] for key in m_data.keys() & {'products','materials'}}
##        for j in m_data:
##            tmp = m_data[j]
##            for k in tmp:
##                df.append([i,j,k['quantity'],k['typeID']]) # need product
##    except KeyError:
##        pass
##df = pd.DataFrame(df)
##df.columns = ['Blueprint ID','Material Type','Quantity','Material ID']
####print(df)
##print('Completed converting blueprints.yaml to JMP table\n')

###################################################
# Extract Production Information
print('Starting to extract production information from blueprints.yaml...')
production = []
for i in blueprints:
    try:
        entry = blueprints[i]
        m_data = entry['activities']['manufacturing']
        m_data = {key: m_data[key] for key in m_data.keys() & {'products','materials','skills'}}
        for j in m_data:
            tmp = m_data[j]
            for k in tmp:
                try:
                    production.append([i,j,k['quantity'],k['typeID']]) # need product
                except KeyError:
                    production.append([i,j,k['level'],k['typeID']])
    except KeyError:
        pass
production = pd.DataFrame(production)
production.columns = ['Blueprint ID','Material Type','Quantity','Material ID']
##print(df)
##production.to_csv('blueprints - production typeIDs.csv', index=False)
print('Completed extracting production information from blueprints.yaml\n'+\
      '\tsee: blueprints - production typeIDs.csv\n\n')
##sys.exit()

##################################
# Extract invention information
print('Starting to extract invention information from blueprints.yaml...')
invention = []
for i in blueprints:
##    print('\nBlueprint typeID: %s\n'%i)
    try:
        entry = blueprints[i]
        m_data = entry['activities']['invention']
##        print('Invention:\n'+str(m_data)+'\n')
##        sys.exit()
        m_data = {key: m_data[key] for key in m_data.keys() & {'products','materials','skills'}}
        for j in m_data:
            tmp = m_data[j]
##            print('Materials:\n'+str(tmp)+'\n')
##            sys.exit()
            for k in tmp:
                try:
                    invention.append([i,j,k['quantity'],k['typeID']]) # need product
                except KeyError:
                    invention.append([i,j,k['level'],k['typeID']])
    except KeyError:
        pass
invention = pd.DataFrame(invention)
##print(invention)
invention.columns = ['Blueprint ID','Material Type','Quantity','Material ID']
print(invention)
##invention.to_csv('blueprints - invention typeIDs.csv', index=False)
print('Completed extracting invention information from blueprints.yaml\n\n')
##sys.exit()

##################################
# Search typeIDs.yaml for corresponding product and material names
print('Starting to load typeIDs.yaml...')
""" Load typeIDs.yaml """
typeIDs = read_yaml('typeIDs.yaml')
print('Completed loading typeIDs.yaml\n')


##################################
# Reference typeIDs to add items to production table
print('Starting to add Material Names to Production table')
material_names = []
for i in range(len(production)):
    try:
        material_names.append(typeIDs[production['Material ID'][i]]['name']['en'])
    except KeyError:
        material_names.append('invalid')
production['Material Name'] = material_names
print(production)
print('Finished adding Material Names to Production table\n')

##################################
# Reference typeIDs to add items to invention table
print('Starting to add Material Names to Invention table')
material_names = []
for i in range(len(invention)):
    try:
        material_names.append(typeIDs[invention['Material ID'][i]]['name']['en'])
    except KeyError:
        material_names.append('invalid')
invention['Material Name'] = material_names
##print(material_names)
print(invention)
##sys.exit()
print('Finished adding Material Names to Invention table\n')

##################################
# Function to generate column of Product Names (querying typeID)
print('Generating column of Product Names (querying typeID)')
def query_product_info(df):
    """ Convert 'Product' row entries to JMP column """
    product_names = []
    product_quantities = []
    product_ids = []
    ##df = invention
    for i in df['Blueprint ID'].drop_duplicates():
        tmp = df[df['Blueprint ID'] == i].copy()
##        print(tmp)
        # add product names
        try:
            product = tmp[tmp['Material Type'] == 'products']['Material Name'].iloc[0]
##            print(product)
        except IndexError:
            product = 'invalid'
        for j in range(len(tmp)):
            try:
                product_names.append(product)
            except IndexError:
                product_names.append('invalid')
                
            # add number of products produced
            try:
                quantity = tmp[tmp['Material Type'] == 'products']['Quantity'].iloc[0]
            except IndexError:
                quantity = 0
            product_quantities.append(quantity)

            # add product typeIDs
            try:
                typeID = tmp[tmp['Material Type'] == 'products']['Material ID'].iloc[0]
    ##            print(quantity)
    ##            sys.exit()
            except IndexError:
                typeID = 0
            product_ids.append(typeID)
            
    df['Product Name'] = product_names
    df['Product Quantity'] = product_quantities
    df['Product typeIDs'] = product_ids
    df = df[df['Material Type'] != 'products']
    df = df[df['Product Name'] != 'invalid']
    return(df)
production = query_product_info(production)
invention = query_product_info(invention)

##################################
# Concatenate production and invention dataframes, and add activity column
print('Concatenating Production and Invention dataframes, and adding activity column\n')
production['activity'] = ['production']*len(production)
invention['activity'] = ['invention']*len(invention)
##print(production)
##print(invention)
df = pd.concat([production, invention]).reset_index(drop=True)
##print(df)
##sys.exit()


##print(df)
print('Completed converting Product rows to column\n')
##sys.exit()
""" Save data as .csv """
try:
    df.to_csv('blueprints.csv',index=False)
except PermissionError:
    input('blueprints.csv is open!  Close it and press Enter.')
print('Data saved as blueprints.csv!')
