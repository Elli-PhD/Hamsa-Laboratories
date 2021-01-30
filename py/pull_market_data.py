import numpy as np
import pandas as pd
# Scrub url pages
import urllib.request

################
# This code pulls market data from Eve Marketer
# 

# Type IDs for all items
# Type IDs modified from Fuzzworks csv
# https://www.fuzzwork.co.uk/resources/typeids.csv
typeids = pd.read_csv('typeids.csv')
typeids.columns = ['ID','Query','x']
typeids.pop('x')
##print(typeids[typeids['Query'] == 'Iron Charge S'])

# load list of items, regions, and systems to query
# configurable csv file
query_list = pd.read_csv('query.csv')
query_list = query_list[query_list['Pull'] == 'y']

# for each item in the query list
# identify typeid
typeid_list = []
for i in range(len(query_list)):
    query = query_list.iloc[i,1]
    typeid_list.append(typeids[typeids['Query'] == query].iloc[0,0])
query_list['IDs'] = typeid_list
print(query_list)
    
    
    
##    id = typeids[typeids['item'] == query.iloc[1,i]]



##https://api.evemarketer.com/ec/marketstat?
##typeid=<typeid>
##<&regionlimit=<regionid>|&usesystem=<systemid>>
