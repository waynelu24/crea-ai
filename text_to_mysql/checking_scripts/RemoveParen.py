# remove lines with (())

f = open("../berkeley_parsed/The_Molecular_Biology_of_the_Cell.txt", 'r')
counter = 0
filename = f.readline()

while filename != '':
	
	filename = filename.rstrip()
	txtfile = open(filename, 'r')
	outputfile = open("../cleaned/" + filename, 'w')
	
	line = txtfile.readline()
	
	while line != '':
		if line == "(())\n" or line == "()\n":
			counter += 1
		else:
			outputfile.write(line)
		
		line = txtfile.readline()
		
	filename = f.readline()
	
print counter
