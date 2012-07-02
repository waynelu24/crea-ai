# call this script at the CREA_AI directory

import os


f = open("checking_scripts/files_to_work_on.txt", 'r')

filename = f.readline()

while filename != '':

	filename = filename.rstrip()
	
	# print "starts parsing %s" % filename
	
	os.system("java -jar berkeleyParser.jar -gr eng_sm6.gr -inputFile split_version/%s > new_parsed/%s" % (filename,filename))
	
	
	print "finished parsing %s" % filename
	
	filename = f.readline()
