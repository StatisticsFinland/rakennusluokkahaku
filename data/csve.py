import pandas as pd
import json

# WARNING MIGHT CHANGE INTEGERS IN CSV TO FLOATS FOR NO APPARENT REASON

#original csv to be edited
df = pd.read_csv("original.csv")

#actual edit. current setup makes columns json formatted for language support
eka = "{"
toka = "}"
df["class_name"] = df["class_name"].apply(lambda x: f'{eka}"fi":"{x}", "sv":"[Svenska]{x}", "en":"[English]{x}"{toka}')
d = [json.loads(x) for x in df["class_name"]]

#creates new file, edit first attribute to choose new file name
df.to_csv("building_classes.csv", sep="," , index = False)

#prints content of new file
df = pd.read_csv("building_classes.csv", sep="," , index = False)
print(df)
d = [json.loads(x) for x in df["class_name"]]
print(d)