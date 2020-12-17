import glob, os
filenames =[]
path=os.path.abspath(__file__ + "/../")
os.chdir(path+"/export/")
for file in glob.glob("*.geojson"):
    filenames.append(file)
    filenames.sort()

with open(path+"/export/"+'output_concatenated_files.geojson', 'w') as outfile:
    with open(filenames[0]) as myfile:
        for index, line in enumerate(myfile):
            if index < 3:
                outfile.write(line)

    for indice,fname in enumerate(filenames):
        with open(fname) as infile:
            num_lines = sum(1 for linea in open(fname))
            for index, line in enumerate(infile):
                if index > 2:

                    if index==num_lines-1 and indice == len(filenames)-1:
                        
                        a=line.strip('\n')
                        
                        b= a.strip(',')
                        
                        outfile.write(b+'\n')
                        outfile.write(']\n')
                        outfile.write('}\n')
                    
                    else:
                        outfile.write(line)


with open(path+"/export/"+'output_concatenated_files.geojson', 'r') as infile:
    buf = infile.readlines()

with open(path+"/export/"+'output_concatenated_files.geojson', 'w') as outfile:
    for line in buf:
        print(line)
        if "FeatureCollection" in line:
            line = line + '"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::3857" } },\n'
        outfile.write(line)
