'''
Split the text files into a sentence per line.
A text file should be a line of string that comprises a chapter of text.
Delimiter = '.' but need to be careful with abbreviations.
'''


f = open("The_Molecular_Biology_of_the_Cell.txt", 'r')


filename = f.readline()

while filename != '':
	
	filename = filename.rstrip()
	textfile = open("original/" + filename, 'r')
	outputFile = open("split_version/" + filename, 'w')  # -4 because we want to add "_SPLIT" right before ".txt"
	
	
	
	paragraph = textfile.read() # a string
	sentence = ''
	begin = 0
	end = 0
	
	
	for index in range(len(paragraph)):
		if paragraph[index] == '.':
			if index + 2 >= len(paragraph):  # at last sentence; + 2 because index starts from 0 and that there's a '\n' at the very end
				# write sentence to outputFile
				sentence = paragraph[begin:end+1]
				outputFile.write(sentence)  # dont need a newline at the last sentence
				# program ends
			elif paragraph[index + 2].isupper():  # '.' used as period if the first letter right after the period is in uppercase
				# write sentence to outputFile
				sentence = paragraph[begin:end+1]
				outputFile.write(sentence + '\n')
				# clear begin and end index
				begin = end + 2
				end += 1
				
			else:	# '.' used for abbreviation
				end += 1
		else:
			end += 1



	filename = f.readline()
