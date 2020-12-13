import json
import os


path=os.path.abspath(__file__ +  "/../" )

print(path)

os.chdir(path+'/export/')

print("Current Working Directory " , os.getcwd())

with open('output_concatenated_files.geojson') as f:
    d = json.load(f)
    print(d)



