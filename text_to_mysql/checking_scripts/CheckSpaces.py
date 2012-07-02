filename = "The_Molecular_Biology_of_the_Cell.txt"
f = open(filename, 'r')


filename = f.readline()

while filename != '':
	
	filename = filename.rstrip()
	txtfile = open(filename, 'r')
	# outputfile = open("original/" + filename, 'w')
	
	line = txtfile.readline()
	lineNum = 1
	containsExtraSpaces = False
	
	while line != '':
		
		if '  ' in line:
			#print "%s line %d has double spaces" % (filename[11:-4],lineNum)
			#print filename
			containsExtraSpaces = True
			break;
		
		line = txtfile.readline()
		lineNum += 1
		
	if containsExtraSpaces:
		print filename
		
	filename = f.readline()
	
	


