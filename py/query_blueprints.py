import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
import sys

# Pull global dataframe of all products and materials
all_mats = pd.read_csv('global - list of materials and products.csv')

# Pull query information from .csv file and add to list
query = pd.read_csv('query_blueprints - query list.csv')
query = query[query['Query'] == 'y']
query['Quantity'] = query['Quantity'].astype(float)
query['ME'] = query['ME'].astype(float)


# Load all blueprint data
blueprints = pd.read_csv('blueprints.csv')
blueprints = blueprints[\
                ['Quantity', 'Material Name', 'Product Name']]
blueprints['Quantity'] = blueprints['Quantity'].astype(float)


# Extract query data from blueprint data
tier1 = pd.DataFrame()
for i in query['Name'].to_list():
    tier1 = pd.concat([tier1, blueprints[\
                                blueprints['Product Name'] == i]])
##print('Tier 1 List')
##print(tier1)

# Save list of materials (w/o duplicates)
# Useful for generating/updating the following file:
# 'global - list of materials and products.csv'
##print(len(tier1['Material Name'].to_list()))
##tier1.drop_duplicates(subset=['Material Name'])\
##    .to_csv('query_blueprints - tier1 mat list.csv')


# Multiply 'Material Name' lists by quantities per item and
# Material Efficiency Factor and round up
# Item quantities configured in query file
tier2 = pd.DataFrame()
for i in tier1['Product Name'].drop_duplicates():
    tmp = tier1[tier1['Product Name'] == i].copy()
    mef = query[query['Name'] == i]['ME'].iloc[0]
    quantity = query[query['Name'] == i]['Quantity'].iloc[0]
##    tmp['Quantity'] = np.ceil(tmp['Quantity']*quantity)
##    tmp['Quantity'] = tmp['Quantity']*quantity*(1-mef/100.)
    tmp['Quantity'] = np.ceil(tmp['Quantity']*quantity*(1-mef/100.))
    tier2 = pd.concat([tier2, tmp])
print(tier1[['Quantity','Material Name']])
print(tier2)
##sys.exit()

# Add unique material quantities together
tier3 = []
for i in tier2['Material Name'].drop_duplicates():
    tmp = tier2[tier2['Material Name'] == i].copy()
    mat = tmp['Material Name'].drop_duplicates().tolist()[0]
    total_quantity = np.sum(tmp['Quantity'])
    tier3.append([total_quantity, mat])
tier3 = pd.DataFrame(tier3)
tier3.columns = ['Quantity','Material Name']
print(tier3)



########################################################
# Print list of items that are related to Planetary Industry
########################################################
print("Planetary Industry Items - Tier 1")
for i in tier3['Material Name'].drop_duplicates():
    if i in all_mats['PI'].to_list():
        print(i)
    else:
        pass
sys.exit()

# parse tier3 dataframe
# if input is a product, query product to find next tier or materials
# if material is a raw material, add to tier2 dataframe
##print(tier1.columns)
##print(all_mats)
# step through tier1 list
# if Material Name is a raw material, add to df
# if Material Name is a product, search blueprints for product materials
tier4 = pd.DataFrame()
for i in tier3['Material Name'].drop_duplicates():
    if i in all_mats['Raw material name'].to_list():
        print(i)
    else:
        pass
##    mat_name = tier2['Material Name'].iloc[i]
##    if mat_name in all_mats['Raw material name'].tolist():
####        print(mat_name)
##        print(tier2.iloc[i,:])
##        sys.exit()
####        tier2 = pd.concat([tier2, pd.DataFrame(tier1.iloc[i,:])], axis=0)
####        print(tier1.iloc[i,:])
##    else:
####        print(blueprints[blueprints['Product Name'] == mat_name])
##        pass
##tier3.to_csv('tmp.csv')



