import numpy as np
import pandas as pd
import sys

# load market_data.csv and blueprints.csv
market_data = pd.read_csv('market_data.csv')
blueprints_all = pd.read_csv('blueprints.csv')
# print data
##print(market_data)
##print(blueprints_all)

query = market_data[market_data['Pull'] == 'y']
##print(query)

# filter blueprint list by query list
blueprints = blueprints_all[blueprints_all['Product Name'].isin(query['Name'])]
##print(blueprints)
##sys.exit()

# for each product calculate cost of materials and append to market_data_all

# pull blueprint data for blueprints in query
products = blueprints['Product Name'].drop_duplicates()

# for each of these products...
for i in products:
    total_cost = 0
    
    # pull dataframe of materials
    material_df = blueprints[blueprints['Product Name'] == i]
##    print(material_df)
##    sys.exit()
    product_quantity = material_df['Product typeIDs'].iloc[0]
##    print(product_quantity)
##    sys.exit()

    # for each material...
    for j in material_df['Material Name'].drop_duplicates():

        # multiply cost by quantity and add to total cost
        cost = market_data[market_data['Name'] == j]['Current highest'].iloc[0]
        quantity = material_df[material_df['Material Name'] == j]['Quantity'].iloc[0]
        total_cost += cost*quantity
##        print(i)
##        print(j)
##        print(cost)
##        print(quantity)
##        print(total_cost)
##    print(i)
##    print(total_cost)
##    print('\n')
    market_data.loc[market_data['Name'] == i,'Cost'] = total_cost
    
# Add number of products produced by blueprint
market_data['Profit'] = product_quantity*market_data['Current lowest'] - market_data['Cost']
##print(blueprints)
##sys.exit()
market_data.to_csv('Profit analysis.csv',index=False)
        
