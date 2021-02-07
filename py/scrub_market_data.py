import numpy as np
import pandas as pd
import sys
# Scrub url pages
import urllib.request

################
## This code pulls market data from Eve Swagger Index (ESI)
##
## webpage format used for scrubbing:
##https://api.evemarketer.com/ec/marketstat?
##typeid=<typeid>
##<&regionlimit=<regionid>|&usesystem=<systemid>>

# load queries
queries = pd.read_csv('queries.csv')

# load blueprint data
blueprints = pd.read_csv('blueprints.csv')

# import typeIDs to queries
for i in range(len(queries)):
    if pd.isnull(queries['ID'][i]) == True:
        queries.loc[i,'ID'] = blueprints[blueprints['Material Name'] == \
                                         queries['Name'][i]]['Material ID'].iloc[0]
    else:
        pass
queries['ID'] = queries['ID'].astype(int)

# pull region ID
region = queries[(queries['Pull'] == 'y') &
                 (queries['Type'] == 'regionID')]['ID'].iloc[0].astype(int)

# trace log: print region info
print(queries[(queries['Pull'] == 'y') &
                 (queries['Type'] == 'regionID')])

for i in range(len(queries)):
    if queries.loc[i,'Type'] != 'typeID':
        pass
    else:
        
        # trace log: print current item name
        print(queries.loc[i,'Name'])

        # pull market data for current item and convert into dataframe
        webpage = urllib.request.urlopen('https://esi.evetech.net/latest/markets/%s'%region+
                                     '/history/?datasource=tranquility&type_id=%s'%queries.loc[i,'ID']).read()
        # need .decode('utf-8') because of b' at the start of the webpage html
        df = pd.DataFrame(list(eval(webpage.decode('utf-8'))))
        
        # copy average item price to query dataframe
        queries.loc[i,'Current average'] = df['average'].iloc[-1]

queries = queries.drop(['Pull'],axis=1)
queries = queries[queries['Type'] == 'typeID']
print('The following data will be saved in market_data.csv')
queries.to_csv('market_data.csv', index=False)
print(queries)

