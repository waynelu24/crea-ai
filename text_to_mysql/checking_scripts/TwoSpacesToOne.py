f = open("../checking_scripts/files_with_extra_spaces.txt", 'r')


filename = f.readline()

while filename != '':
	
	filename = filename.rstrip()
	txtfile = open(filename, 'r')
	outputfile = open("../cleaned/" + filename, 'w')
	
	line = txtfile.readline()
	
	while line != '':
		lineToWrite = line.replace("  ",' ')
		
		outputfile.write(lineToWrite)
		
		line = txtfile.readline()
		
	filename = f.readline()
