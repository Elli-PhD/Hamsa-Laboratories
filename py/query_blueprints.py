import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
import sys

# Pull global dataframe of all products and materials
all_mats = pd.read_csv('global - list of materials and products.csv',\
                       header = 0, encoding = 'unicode_escape')

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
##tier1 = pd.DataFrame()
##for i in query['Name'].to_list():
##    tier1 = pd.concat([tier1, blueprints[\
##                                blueprints['Product Name'] == i]])


# This should be a recursive algorithm
# Take the initial list of material requirements
# Parse it into PI, Raw Materials, and Product lists
# Repeat with subsequent Product lists, appending to PI and Raw Material lists until Product lists is empty
base = pd.DataFrame()
products = pd.DataFrame()
for i in query['Name'].to_list():
    base = pd.concat([base, blueprints[\
                                blueprints['Product Name'] == i]])

# Multiply base list by ME and quantities
products = pd.DataFrame()
for i in base['Product Name'].drop_duplicates():
    tmp = base[base['Product Name'] == i].copy()
    mef = query[query['Name'] == i]['ME'].iloc[0]
    quantity = query[query['Name'] == i]['Quantity'].iloc[0]
##    tmp['Quantity'] = np.ceil(tmp['Quantity']*quantity)
##    tmp['Quantity'] = tmp['Quantity']*quantity*(1-mef/100.)
    tmp['Quantity'] = np.ceil(tmp['Quantity']*quantity*(1-mef/100.))
    products = pd.concat([products, tmp])

# Add unique material quantities together
products_tmp = []
for i in products['Material Name'].drop_duplicates():
    tmp = products[products['Material Name'] == i].copy()
    mat = tmp['Material Name'].drop_duplicates().tolist()[0]
    total_quantity = np.sum(tmp['Quantity'])
    products_tmp.append([total_quantity, mat])
products_tmp = pd.DataFrame(products_tmp)
products_tmp.columns = ['Quantity','Material Name']
products = products_tmp

##products = base
iteration = 0
print('Base list (iteration = %s):'%iteration)
print(base)
print('\n\n')
print('Product list (item quantities and ME applied; Iteration = %s, length = %s)'%(iteration,len(products)))
print(products)
print('\n\n')

# In products, extract PI, Raw materials, and products
# Take for products, query building materials and append to PI, Raw Materials, and generate new products
# repeat until list contains only raw materials
# Seperate list of Planetary Industry materials from other materials
pi_list = products[products['Material Name'].isin(all_mats['PI-all-items'].tolist())\
                == True]
# Seperate raw materials from products
raw_materials = products[products['Material Name'].isin(all_mats['Raw material name'].tolist())\
                == True]
# Seperate Items that require further breakdown
products = products[(products['Material Name'].isin(all_mats['PI-all-items'].tolist())\
                == False) & \
                   (products['Material Name'].isin(all_mats['Raw material name'].tolist())\
                == False)]

print('Planetary Industry (iteration = %s):'%iteration)
print(pi_list)
print('\n\n')
print('Other raw materials (iteration = %s):'%iteration)
print(raw_materials)
print('\n\n')
print("Remaining products (iteration = %s, length = %s)"%(iteration, len(products)))
print(products)
print('\n\n')

# Iterative process starts here
# Generate Base List
base_tmp = pd.DataFrame()
for i in products['Material Name'].to_list():
    base_tmp = pd.concat([base_tmp, blueprints[\
                                blueprints['Product Name'] == i]])
iteration =+ 1
print('Base (base_tmp, iteration = %s)'%iteration)
print(base_tmp)
print('\n\n')
# Multiply each Material by number of associated products and ME (assume ME=10)
products_tmp = pd.DataFrame()
for i in base_tmp['Product Name'].drop_duplicates():
    tmp = base_tmp[base_tmp['Product Name'] == i].copy()
    quantity = products[products['Material Name'] == i]['Quantity'].iloc[0]
##    print(quantity)
##    # Keep this for future reference; I may need to make a list of ME values in the future
##    mef = query[query['Name'] == i]['ME'].iloc[0]
##    tmp['Quantity'] = np.ceil(tmp['Quantity']*quantity*(1-mef/100.))
    tmp['Quantity'] = np.ceil(tmp['Quantity']*quantity*0.9)
    products_tmp = pd.concat([products_tmp, tmp])
products = products_tmp
##print('Base times quantities and ME (products, iteration = %s)'%iteration)
##print(products)
##print('\n\n')

# Add unique material quantities together
products_tmp = []
for i in products['Material Name'].drop_duplicates():
    tmp = products[products['Material Name'] == i].copy()
    mat = tmp['Material Name'].drop_duplicates().tolist()[0]
    total_quantity = np.sum(tmp['Quantity'])
    products_tmp.append([total_quantity, mat])
products = pd.DataFrame(products_tmp)
products.columns = ['Quantity','Material Name']
print('Product list (item quantities and ME applied; iteration = %s)'%iteration)
print(products)
print('\n\n')

# Place contents of products_tmp into respective [tmp] dataframes (PI, Raw, and Products)
# variables to recall: pi_list, raw_materials
# Seperate list of Planetary Industry materials from other materials
pi_list_tmp = products[products['Material Name'].isin(all_mats['PI-all-items'].tolist())\
                == True]
# Seperate raw materials from products
raw_materials_tmp = products[products['Material Name'].isin(all_mats['Tier 1'].tolist())\
                == True]
# Seperate Items that require further breakdown
products_tmp = products[(products['Material Name'].isin(all_mats['PI-all-items'].tolist())\
                == False) & \
                   (products['Material Name'].isin(all_mats['Raw material name'].tolist())\
                == False)]
##print(pi_list_tmp)
##print(raw_materials_tmp)

# Append tmp contents to base contents (PI and Raw)
pi_list = pd.concat([pi_list, pi_list_tmp])
raw_materials = pd.concat([raw_materials, raw_materials_tmp])
##print(pi_list)
##print(raw_materials)

# Add unique PI material quantities together
##print(pi_list)
pi_list_tmp = []
for i in pi_list['Material Name'].drop_duplicates():
    tmp = pi_list[pi_list['Material Name'] == i].copy()
    total_quantity = np.sum(tmp['Quantity']).astype(float)
    mat = tmp['Material Name'].iloc[0]
    pi_list_tmp.append([total_quantity, mat])

pi_list = pi_list_tmp
pi_list = pd.DataFrame(pi_list)
pi_list.columns = ['Quantity','Material Name']
pi_list = pi_list.sort_values(by = 'Material Name')
##print(pi_list)
##sys.exit()
    
# Add unique raw material quantities together
##print(raw_materials)
raw_materials_tmp = []
for i in raw_materials['Material Name'].drop_duplicates():
    tmp = raw_materials[raw_materials['Material Name'] == i].copy()
    total_quantity = np.sum(tmp['Quantity']).astype(float)
    mat = tmp['Material Name'].iloc[0]
    raw_materials_tmp.append([total_quantity, mat])

raw_materials = raw_materials_tmp
raw_materials = pd.DataFrame(raw_materials)
raw_materials.columns = ['Quantity','Material Name']
raw_materials = raw_materials.sort_values(by = 'Material Name')

# Split raw_materials into mineral, salvage, and advanced moon materials
minerals = raw_materials[raw_materials['Material Name'].\
                         isin(all_mats['Minerals'].tolist())]
adv_moon_mats = raw_materials[raw_materials['Material Name'].\
                         isin(all_mats['Advanced Moon Materials'].tolist())]
salvage = raw_materials[raw_materials['Material Name'].\
                         isin(all_mats['Salvage'].tolist())]


print('Final report: \n')
print('Base list (iteration = 0)')
print(base)
print('\n\n')
print('Planetary Industry: ')
print(pi_list)
print('\n\n')
print('Minerals: ')
print(minerals)
print('\n\n')
print('Advanced Moon Materials: ')
print(adv_moon_mats)
print('\n\n')
print('Salvage: ')
print(salvage)

input('Press Enter to exit...')
sys.exit()
    




















# Seperate list of Planetary Industry materials from other materials
pi_list = tier3[tier3['Material Name'].isin(all_mats['PI-all-items'].tolist())\
                == True]
# Seperate raw materials from products
raw_materials = tier3[tier3['Material Name'].isin(all_mats['Raw material name'].tolist())\
                == True]
# Seperate Items that require further breakdown
to_process = tier3[(tier3['Material Name'].isin(all_mats['PI-all-items'].tolist())\
                == False) & \
                   (tier3['Material Name'].isin(all_mats['Raw material name'].tolist())\
                == False)]







##while len(products) != 0:
# Multiply 'Material Name' lists by quantities per item and
# Material Efficiency Factor and round up
# Item quantities configured in query file
tier2 = pd.DataFrame()
for i in products['Product Name'].drop_duplicates():
    tmp = products[products['Product Name'] == i].copy()
    mef = query[query['Name'] == i]['ME'].iloc[0]
    quantity = query[query['Name'] == i]['Quantity'].iloc[0]
##    tmp['Quantity'] = np.ceil(tmp['Quantity']*quantity)
##    tmp['Quantity'] = tmp['Quantity']*quantity*(1-mef/100.)
    tmp['Quantity'] = np.ceil(tmp['Quantity']*quantity*(1-mef/100.))
    tier2 = pd.concat([tier2, tmp])
print(tier2)

sys.exit()



# Extract PI-specific information


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
##print(tier2)
##print('\n\n')
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




# Seperate list of Planetary Industry materials from other materials
pi_list = tier3[tier3['Material Name'].isin(all_mats['PI-all-items'].tolist())\
                == True]
# Seperate raw materials from products
raw_materials = tier3[tier3['Material Name'].isin(all_mats['Raw material name'].tolist())\
                == True]
# Seperate Items that require further breakdown
to_process = tier3[(tier3['Material Name'].isin(all_mats['PI-all-items'].tolist())\
                == False) & \
                   (tier3['Material Name'].isin(all_mats['Raw material name'].tolist())\
                == False)]

# Identify materials required to build each product
tier2 = pd.DataFrame()
for i in to_process['Material Name'].to_list():
    tier2 = pd.concat([tier2, blueprints[\
                                blueprints['Product Name'] == i]])

# Multiply by ME and quantities



print('Query List')
print(query[['Name', 'Quantity']])
print('\n\n')
print('Tier 1 (non-PI)')
print(tier3)
print('\n\n')
print("Tier 1 (PI)")
print(pi_list)
print('\n\n')
print("Tier 1 (raw materials)")
print(raw_materials)
print('\n\n')
print("Tier 1 (Items that require identifying raw materials)")
print(to_process)
print('\n\n')
print("Tier 2")
print(tier2[''])
print('\n\n')




########################################################
# Print list of items that are related to Planetary Industry
########################################################
##for i in pi_list['Material Name'].drop_duplicates():
##    if i in all_mats['PI-all-items'].to_list():
##        print(i)
##    else:
##        pass
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



