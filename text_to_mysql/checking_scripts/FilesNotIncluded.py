biggerFile = open("../split_version/The_Molecular_Biology_of_the_Cell.txt", 'r')
smallerFile = open("../berkeley_parsed/The_Molecular_Biology_of_the_Cell.txt", 'r')


biggerFileList = biggerFile.readlines()
smallerFileList = smallerFile.readlines()

newBigger = []
newSmaller = []

#chomping

for filename in biggerFileList:
	newBigger.append(filename.rstrip())
	
for filename in smallerFileList:
	newSmaller.append(filename.rstrip())
	


# actual checking
for filename in newBigger:
	if filename not in newSmaller:
		print filename
