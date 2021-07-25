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
print('Completed loading blueprints.yaml\n')

print('Starting to convert blueprints.yaml to JMP table...')
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
df = []
for i in blueprints:
    try:
        entry = blueprints[i]
        m_data = entry['activities']['manufacturing']
        m_data = {key: m_data[key] for key in m_data.keys() & {'products','materials','skills'}}
        for j in m_data:
            tmp = m_data[j]
            for k in tmp:
                try:
                    df.append([i,j,k['quantity'],k['typeID']]) # need product
                except KeyError:
                    df.append([i,j,k['level'],k['typeID']])
    except KeyError:
        pass
df = pd.DataFrame(df)
df.columns = ['Blueprint ID','Material Type','Quantity','Material ID']
##print(df)
df.to_csv('blueprints - typeID indexes.csv')
print('Completed converting blueprints.yaml to JMP table\n')
##sys.exit()

##################################

print('Starting to load typeIDs.yaml...')
""" Load typeIDs.yaml """
typeIDs = read_yaml('typeIDs.yaml')
print('Completed loading typeIDs.yaml\n')

print('Starting to add item names to JMP table...')
material_names = []

""" Reference typeIDs to add item names to JMP table """
for i in range(len(df)):
    try:
        material_names.append(typeIDs[df['Material ID'][i]]['name']['en'])
    except KeyError:
        material_names.append('invalid')
df['Material Name'] = material_names
##print(df)
print('Completed adding item names to JMP table\n')
df.to_csv('tmp.csv',index=False)

##################################
df = pd.read_csv('tmp.csv')

print('Starting to convert Product rows to column...')
""" Convert 'Product' row entries to JMP column """
product_names = []
product_quantities = []
product_ids = []
for i in df['Blueprint ID'].drop_duplicates():
    tmp = df[df['Blueprint ID'] == i].copy()

    try:
        product = tmp[tmp['Material Type'] == 'products']['Material Name'].iloc[0]
##        print(product)
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
##print(df)
print('Completed converting Product rows to column\n')

""" Save data as .csv """
df.to_csv('blueprints.csv',index=False)
print('Data saved as blueprints.csv!')
