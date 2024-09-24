import json, os

#recursively get all of the keys and subkeys in a list organized like class objects for the subgroups
def getkeysandsubkeys(data, keydict, parentkey):
    for a,b in data.items():
        if isinstance(b,dict):
            if parentkey == '':
                newroot = a
            else:
                newroot = parentkey + "." + a
            if newroot not in keydict:
                keydict.append(newroot)
            getkeysandsubkeys(b, keydict, newroot)
        if isinstance(b,list):
            for item in b:
                getkeysandsubkeys(item,keydict,a)
        else:
            if parentkey == '':
                newroot = a
            else:
                newroot = parentkey + "." + a
            if newroot not in keydict:
                keydict.append(newroot)

# Directory where the data is stored
input_directory = ""

parameters = []

for file in os.listdir(input_directory):
    filename = input_directory + os.fsdecode(file)
    if filename.endswith("_Adds"):
        datafile = open(filename, "r")
        content = datafile.read()
        datafile.close()
        data = dict(json.loads(content.encode('unicode_escape').decode('utf-8')))

        getkeysandsubkeys(data,parameters,'')

print(parameters)





