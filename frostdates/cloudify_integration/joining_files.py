import glob, os
filenames =[]
path=os.path.abspath(__file__ + "/../")
os.chdir(path+"/export/")
for file in glob.glob("*.geojson"):
    filenames.append(file)

filenames.sort()

with open(path+"/export/"+'output_concatenated_files.geojson', 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)
