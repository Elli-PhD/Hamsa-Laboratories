import pandas as pd

######################
# this code parses through typeIDs.yaml line-by-line
# and returns each typeID and name combination into a JMP table
######################

def export_typeIDs():
    # open typeIDs.yaml file
    file = open('typeIDs.yaml','r', encoding='utf-8')

    # generate empty list to populate with typeIDs and corresponding names
    typeIDs = []

    # iterate through each line of the file
    # and pull typeIDs and corresponding names
    while True:
        
        # get next line from file
        line = file.readline()

        # if line is empty, end of file has been reached
        if not line:
            break
        # try to extract typeID, which is an integer value followed by ':\n'
        # remove ':\n' from the end of the string and try to convert into integer
        # if this fails, the line does not contain the typeID
        try:
            typeID = int(line[:-2])
        except ValueError:
            pass

        # pull english name using string 'en: '
        # description and name groups both contain 'en: ' string
        # I do not want to pull the description, only the name
        # the pattern in this file is typeID -> description -> name -> typeID -> etc.
        # when the line contains 'description' set marker to 0 ('off')
        # this will skip any 'en: ' entry until the line contains 'name'
        # this will set the marker to 1 ('on'),
        # and the subsequent 'en: ' will be logged
        # the code iterates over each typeID
        if 'description' in line:
            x = 0
        elif 'name' in line:
            x = 1
        else:
            pass
        if 'en: ' in line and x == 1:
            name = line
        elif 'zh:' in line and x == 1:
            # when you arrive at the name/zh: entry,
            # append typeID and name to list
            typeIDs.append([typeID, name])
        else:
            pass

    # convert list to dataframe
    typeIDs = pd.DataFrame(typeIDs)

    # set dataframe columns
    typeIDs.columns = ['typeID', 'Name']

    # remove unwanted characters
    typeIDs['Name'] = typeIDs['Name'].str.replace('en: ','')
    typeIDs['Name'] = typeIDs['Name'].str.replace('\n','')

    # return typeIDs
    return typeIDs
