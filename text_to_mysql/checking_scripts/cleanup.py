f = open("The_Molecular_Biology_of_the_Cell.txt", 'r')


filename = f.readline()

while filename != '':
	
	filename = filename.rstrip()
	txtfile = open(filename, 'r')
	outputfile = open("original/" + filename, 'w')
	
	line = txtfile.readline()
	
	while line != '':
		lineToWrite = line[1:] # take out the space
		lineToWrite = lineToWrite.replace('(','<')
		lineToWrite = lineToWrite.replace(')','>')
		
		outputfile.write(lineToWrite)
		
		line = txtfile.readline()
		
	filename = f.readline()
