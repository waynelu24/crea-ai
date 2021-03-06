'''
run this program in the directory where the text files are stored
do a $ ls > book_name.txt in the directory first and pass that text file's name as the argument to the program
'''

import sys
import getpass
import MySQLdb
import TreeNode	# self-written
import TreeSentenceFunctions #self-written

punctuations = [',', ';', '.', '?', '!', '\'', '\"' ] #, '<', '>']
iamdebugging = False

# take out the punctuation(s) in the word if there's any	
def cleanUpWord(word):

	if word[0] in punctuations:
		word = word[1:]
	if (word != '') and (word[-1] in punctuations):
		word = word[:-1]

	return word

def countNumChildren(lstOfSentencePhraseRelTableEntries,i):
	numChildren = 1
	if len(lstOfSentencePhraseRelTableEntries) - 1 != i:
		parent = lstOfSentencePhraseRelTableEntries[i]
		for entry in lstOfSentencePhraseRelTableEntries[i+1:]:
			if entry.hasSameObjEntry(parent):
				numChildren += 1
			else:
				break
	
	return numChildren


if __name__ == "__main__":
	
	if len(sys.argv) != 2:
		print "ERROR: USAGE SHOULD BE"
		print "$ python ParseTheParse.py text_file_containing_file_names\n"
		sys.exit(1)
	
	print 
	login = raw_input("mysql login: ")
	password = getpass.getpass()
	
	# connect to mysql
	mysqlConnection = MySQLdb.connect('localhost', login, password, 'CREAKB')  # 'CREAKB'
	mysqlCursor = mysqlConnection.cursor()
	
	# sql commands: store book name into book_tbl and get its ID
	mysqlCursor.execute("SELECT book_id FROM book_tbl WHERE book_title = %s", sys.argv[1][:-4]) 
	bookID = mysqlCursor.fetchone()
	if bookID is None:
		mysqlCursor.execute("INSERT INTO book_tbl(book_title) VALUES(%s)", sys.argv[1][:-4]) 
		mysqlCursor.execute("SELECT book_id FROM book_tbl WHERE book_title = %s", sys.argv[1][:-4]) 
		bookID = mysqlCursor.fetchone()
	bookID = int(bookID[0])
	
	fileOfFilenames = open(sys.argv[1], 'r')
	filename = fileOfFilenames.readline()
	
	mysqlConnection.commit()
	
	# going through the files/chapters
	while filename != '':
	
		filename = filename.rstrip() # chomp; remove the '\n' at the end
		chapterName = filename[11:-4] # [11:-4] to strip off "TITLExxxxxxx" and ".txt"
		
		# sql commands: store chapter name into chapter_tbl and get its ID
		mysqlCursor.execute("INSERT INTO chapter_tbl(book_id, chapter_title) VALUES(%s,%s)", (bookID, chapterName))
		mysqlCursor.execute("SELECT chapter_id FROM chapter_tbl WHERE chapter_title = %s", chapterName)
		chapterID = int(mysqlCursor.fetchone()[0])
		mysqlConnection.commit()
		
		parsedChapter = open(filename, 'r')  # a text file that contains lines of parsed sentences
		treeString = parsedChapter.readline()
		sentenceSequence = 0
			
		# going through the lines in a file/chapter
		while treeString != '':
		
			treeRoot = TreeNode.TreeNode.treeStringToTree(treeString) # treeStringToTree is a @staticmethod
			#storeIntoDatabase(treeRoot,sentenceSequence,mysqlCursor)
			sentenceBody = treeRoot.toSentence()
			
			# sql commands: sentence_tbl
			mysqlCursor.execute("INSERT INTO sentence_tbl(chapter_id,sentence_body,sentence_sequence) VALUES(%s,%s,%s)", (chapterID,sentenceBody,sentenceSequence))
			mysqlCursor.execute("SELECT sentence_id FROM sentence_tbl WHERE sentence_body = %s", sentenceBody)
			sentenceID = int(mysqlCursor.fetchone()[0])
			
			mysqlConnection.commit()
			wordAndTag = treeRoot.toTagWordTuple() # a list of (tag word) tuples, ignoring non leaf(word) level nodes
			
			# sql commands for word_tbl and word_POS_tbl
			for tagWordTuple in TreeSentenceFunctions.splitPhrases(wordAndTag):
				decomposedTuple = TreeSentenceFunctions.decomposePhrase(tagWordTuple)
				tag = decomposedTuple[0]
				word = decomposedTuple[1]
				
				# take out the punctuation(s) in the word if there's any
				word = cleanUpWord(word)
				
				if word != '':	
					# sql commands: word_tbl
					mysqlCursor.execute("SELECT word_id from word_tbl where word_name = %s", word)
					wordID = mysqlCursor.fetchone()
					if not wordID: # ensures that entries in word_tbl are unique
						mysqlCursor.execute("INSERT INTO word_tbl(word_name) VALUES(%s)", word)
						mysqlCursor.execute("SELECT word_id FROM word_tbl WHERE word_name = %s", word)
						wordID = mysqlCursor.fetchone()
					wordID = wordID[0]
					
					mysqlConnection.commit()
			
					# sql commands: word_POS_tbl
					mysqlCursor.execute("SELECT word_id from word_POS_tbl where word_name = %s AND word_POS = %s", (word,tag))
					wordPOSTblEntryFound = mysqlCursor.fetchone() # used as boolean
					if not wordPOSTblEntryFound: # ensures that entries in word_POS_tbl are unique
						mysqlCursor.execute("INSERT INTO word_POS_tbl(word_id,word_name,word_POS) VALUES(%s,%s,%s)", (wordID,word,tag))
			
			
					mysqlConnection.commit()
			# sql commands for sentence_phrase_tbl 
			sentencePhraseTableEntries = treeRoot.toLstOfSentencePhraseTableEntries()
			
			if iamdebugging:
				print "printing phraseTable entries:"
				for entry in sentencePhraseTableEntries:
					print entry
				print
			
			for sentencePhraseTableEntry in sentencePhraseTableEntries:
				mysqlCursor.execute("SELECT word_POS_id FROM word_POS_tbl WHERE word_name = %s", sentencePhraseTableEntry.getText())
				wordPOSID = mysqlCursor.fetchone()
				if wordPOSID is None:
					mysqlCursor.execute("INSERT INTO sentence_phrase_tbl(sentence_id,sentence_phrase_text,sentence_phrase_text_TAG) VALUES(%s,%s,%s)", (sentenceID,sentencePhraseTableEntry.getText(),sentencePhraseTableEntry.getTag())) 
				else:
					wordPOSID = wordPOSID[0]
					mysqlCursor.execute("INSERT INTO sentence_phrase_tbl(sentence_id,word_POS_id,sentence_phrase_text,sentence_phrase_text_TAG) VALUES(%s,%s,%s,%s)", (sentenceID,wordPOSID,sentencePhraseTableEntry.getText(),sentencePhraseTableEntry.getTag())) 
			
			mysqlConnection.commit()
			
			if iamdebugging:
				mysqlCursor.execute("SELECT * FROM sentence_phrase_tbl")
				sentence_phrase_tbl_entries = mysqlCursor.fetchall()
				print "printing sentence_phrase_tbl entries"
				for entry in sentence_phrase_tbl_entries:
					print entry
				print 
			
			
			# sql commands for sentence_phrase_rel_tbl
			sentencePhraseRelTableEntries = treeRoot.toLstOfSentencePhraseRelTableEntries()
			occuredTagsObj = {} # used to keep track of phrases with empty text	
			occuredTagsTarget = {} # e.g. {('', ''): 1, ('NP', ''): 3}
			stopAt = 0 # used to keep track of phrases with empty text		

			i = 0 # used for indexing in the for loop below
			lastSentencePhraseRelTableEntry = None
			numChildren = None
			nthChildren = None
			
			if iamdebugging:
				print "printing sentencePhraseRelTable entries"
				for entry in sentencePhraseRelTableEntries:
					print entry
				print
			
			### assumes no 2 consecutive same phrase tag (e.g. entry 1's tag == NP and entry 2's tag == NP)			
			for sentencePhraseRelTableEntry in sentencePhraseRelTableEntries:
				if iamdebugging:
					print "\n\n"
					

				# get obj_phrase_id
				objEntry = sentencePhraseRelTableEntry.getObjEntry()
				
				if iamdebugging:
					print "lastSentencePhraseRelTableEntry = %s" % str(lastSentencePhraseRelTableEntry)
					print "sentencePhraseRelTableEntry = %s" % str(sentencePhraseRelTableEntry)
					if lastSentencePhraseRelTableEntry is not None:
						print "lastSentencePhraseRelTableEntry.hasSameObjEntry(sentencePhraseRelTableEntry) returns %s" % str(lastSentencePhraseRelTableEntry.hasSameObjEntry(sentencePhraseRelTableEntry))
				
				if (lastSentencePhraseRelTableEntry is None) or (not lastSentencePhraseRelTableEntry.hasSameObjEntry(sentencePhraseRelTableEntry)):
					
					numChildren = countNumChildren(sentencePhraseRelTableEntries,i) # set numChildren
					if iamdebugging:
						print "%s's numChildren = %d" % (str(objEntry),numChildren)
						print "occuredTagsObj: ",
						print occuredTagsObj
						if (objEntry.getTag(),objEntry.getText()) not in occuredTagsObj:
							print "%s not in occuredTagsObj" % str((objEntry.getTag(),objEntry.getText()))
						else:
							print "%s is in occuredTagsObj" % str((objEntry.getTag(),objEntry.getText()))
					
					nthChildren = 1 # initialize to 1 because working on the first child at this stage
					
					if (objEntry.getTag(),objEntry.getText()) not in occuredTagsObj:
						occuredTagsObj[(objEntry.getTag(),objEntry.getText())] = 0 # insert into occuredTagsObj
						stopAt = 0 # set stopAt to 0
					else:
						stopAt = occuredTagsObj[(objEntry.getTag(),objEntry.getText())]
					
					if numChildren < 2:
						occuredTagsObj[(objEntry.getTag(),objEntry.getText())] += 1
					
					occuredTagsTarget = {} # clear occuredTagsTarget
					
				else:
					# compare with numChildren
					nthChildren += 1
					if nthChildren == numChildren:
						# increment nthChildren
						occuredTagsObj[(objEntry.getTag(),objEntry.getText())] += 1
						# TODO: possibly take out the line below						
						###stopAt = occuredTagsObj[(objEntry.getTag(),objEntry.getText())] # increment stopAt
				

				
				if objEntry.getText() == '':
					mysqlCursor.execute("SELECT sentence_phrase_id FROM sentence_phrase_tbl WHERE sentence_id = %s AND word_POS_id is NULL AND sentence_phrase_text = %s AND sentence_phrase_text_TAG = %s", (sentenceID,objEntry.getText(),objEntry.getTag()))
				else:
					mysqlCursor.execute("SELECT sentence_phrase_id FROM sentence_phrase_tbl WHERE sentence_id = %s AND sentence_phrase_text = %s AND sentence_phrase_text_TAG = %s", (sentenceID,objEntry.getText(),objEntry.getTag())) # and word_POS_id = %s
					
				objPhraseID = mysqlCursor.fetchall() 
				
				if iamdebugging:
					
					print "obj choices: ",
					print objPhraseID
					print "stopAt = %d" % stopAt
					
				
				objPhraseID = objPhraseID[stopAt][0]
				
				
				
				
				
				
				# get target_phrase_id	
				targetEntry = sentencePhraseRelTableEntry.getTargetEntry()
				if targetEntry.getText() == '':
					mysqlCursor.execute("SELECT sentence_phrase_id FROM sentence_phrase_tbl WHERE sentence_id = %s AND word_POS_id is NULL AND sentence_phrase_text = %s AND sentence_phrase_text_TAG = %s", (sentenceID,targetEntry.getText(),targetEntry.getTag()))
				else:
					mysqlCursor.execute("SELECT sentence_phrase_id FROM sentence_phrase_tbl WHERE sentence_id = %s AND sentence_phrase_text = %s AND sentence_phrase_text_TAG = %s", (sentenceID,targetEntry.getText(),targetEntry.getTag())) # and word_POS_id = %s
				
				
				targetPhraseID = mysqlCursor.fetchall() 
				
				if iamdebugging:
					print "target choices",
					print targetPhraseID
					print "nthChildren = %d" % nthChildren
				
				if len(targetPhraseID) == 1:
					targetPhraseID = targetPhraseID[0][0]
				else:	
					skipOver = 0
					if (targetEntry.getText(), targetEntry.getTag()) in occuredTagsTarget:
						skipOver = occuredTagsTarget[(targetEntry.getText(), targetEntry.getTag())]
					if iamdebugging:
						print "skipOver = %d" % skipOver
					for index in range(len(targetPhraseID)):
						if objPhraseID < targetPhraseID[index][0]:
							if skipOver == 0:
								targetPhraseID = targetPhraseID[index][0]	
								# increment occuredTagsTarget
								if (targetEntry.getText(), targetEntry.getTag()) not in occuredTagsTarget:
									occuredTagsTarget[targetEntry.getText(), targetEntry.getTag()] = 1
								else:
									occuredTagsTarget[targetEntry.getText(), targetEntry.getTag()] += 1
								break
							else:
								skipOver -= 1
				
				
				
				if iamdebugging:
					print "sid = %s, objid = %s, tid = %s" % (sentenceID,objPhraseID,targetPhraseID)
				
				# insert entry
				mysqlCursor.execute("INSERT INTO sentence_phrase_rel_tbl(sentence_id,object_phrase_id,target_phrase_id,phrase_rel_level_vert,phrase_rel_level_horz) VALUES(%s,%s,%s,%s,%s)", (sentenceID,objPhraseID,targetPhraseID,sentencePhraseRelTableEntry.getVertLvl(),sentencePhraseRelTableEntry.getHoriLvl()))
			
				lastSentencePhraseRelTableEntry = sentencePhraseRelTableEntry
				i += 1
				
				if iamdebugging:
					raw_input() # "break point" for debugging
				# end for loop
			
			treeString = parsedChapter.readline()
			sentenceSequence += 1
		
		mysqlConnection.commit()
		print "finished parsing %s" % filename
		filename = fileOfFilenames.readline()
		

	
	mysqlConnection.close()


