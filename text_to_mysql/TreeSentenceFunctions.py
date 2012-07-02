import re


def isLeafLevel(treeString):
	level = 1

	for char in treeString[1:]:
		if char == '(':
			level += 1
			if level > 1:
				return False
		elif char == ')':
			level -= 1
			
	
	return True

'''
returns the split phrases in a list (of strings)
each phrase has only 1 top level tag
'''
def splitPhrases(treeString):
	if hasOneTopLevelPhrase(treeString):
		return [treeString]
		
	level = 1
	index = 1
	begin = 0
	end = 0
	lstOfPhrases = []
	
	for char in treeString[1:]:
		if char == '(':
			level += 1
			if level == 1:
				begin = index
		elif char == ')':
			level -= 1
			if level == 0:
				end = index
				lstOfPhrases.append(treeString[begin:end] + ')')
		
		
		index += 1	

	return lstOfPhrases
	
# helper function for splitPhrases()
def hasOneTopLevelPhrase(treeString):
	level = 1
	numTopLevelPhrase = 0

	for char in treeString[1:]:
		if char == '(':
			if level == 0:
				return False
			level += 1

		elif char == ')':
			level -= 1
			
	return True

# argument = treeString with only 1 top level phrase 
def getTopLevelTag(treeString):
	matchObj = re.match("\([A-Z]{0,10}[\$\.]{0,1} ", treeString)
	return matchObj.group()[1:-1]



def stripOneLevel(treeString):
	level = 1
	stripIndices = [0]
	index = 1
	
	# finding out the places to strip
	for char in treeString[1:]:
		if char == '(':
			level += 1
		elif char == ')':
			level -= 1
			if level == 0:
				stripIndices.append(index)
		elif level == 1:
			stripIndices.append(index)
		
		index += 1		
	
	# creating the stripped string
	newString = ''
	
	
	for i in range(len(treeString)):
		if (len(stripIndices) == 0) or  (i != stripIndices[0]):
		#if i != stripIndices[0]:
			newString += treeString[i]
		else: 
			del stripIndices[0]
			
	newString = newString.replace(")(", ") (")
	return newString


# phrase = a string of tuple of tag and word; e.g.  "(DT The)"
def decomposePhrase(phrase):
	splitTuple = phrase.split(' ')  # e.g. ["(DT", "The)"]
	#print splitTuple # debugging
	tag = splitTuple[0][1:]
	word = splitTuple[1][:-1]
	return (tag,word)





### test cases
if __name__ == "__main__":
	
	'''
	s = "( (S (NP (DT The) (JJ quick) (JJ brown) (NN fox)) (VP (VBZ jumps) (PP (IN over) (NP (DT the) (JJ lazy) (NN dog))))) )"
	s2 = "(S (NP (DT The) (JJ quick) (JJ brown) (NN fox)) (VP (VBZ jumps) (PP (IN over) (NP (DT the) (JJ lazy) (NN dog)))))"
	s3 = "(NP (DT The) (JJ quick) (JJ brown) (NN fox)) (VP (VBZ jumps) (PP (IN over) (NP (DT the) (JJ lazy) (NN dog))))"
	s4 = "(DT The) (JJ quick) (JJ brown) (NN fox) (VBZ jumps) (PP (IN over) (NP (DT the) (JJ lazy) (NN dog)))"
	s5 = "(DT The) (JJ quick) (JJ brown) (NN fox) (VBZ jumps) (IN over) (NP (DT the) (JJ lazy) (NN dog))"
	s6 = "(DT The) (JJ quick) (JJ brown) (NN fox) (VBZ jumps) (IN over) (DT the) (JJ lazy) (NN dog)"

	lst = [s,s2,s3,s4,s5,s6]


	for string in lst:
		print splitPhrases(string)
		#print getTopLevelTag(string)
		#print "%d\n %s\n\n\n" % (len(x),x)
		#print hasOneTopLevelPhrase(string)
		#print isLeafLevel(string)
	'''

	'''
	print stripOneLevel(s) == s2
	print stripOneLevel(s2) == s3
	print stripOneLevel(s3) == s4
	print stripOneLevel(s4) == s5
	print stripOneLevel(s5) == s6
	'''
	
	# testing decomposePhrase
	'''
	testDecomposePhrase_string = "(DT The)"
	print decomposePhrase(testDecomposePhrase_string)
	'''
	
	# testing splitPhrases()
	'''
	s = "(S (NP (DT The) (JJ quick) (JJ brown) (NN fox)))"
	s2 = "(NP (DT The) (JJ quick) (JJ brown) (NN fox))"
	print splitPhrases(s)
	'''
	
	# testing getTopLevelTag()
	'''
	s = "( (S (NP (DT The) (JJ quick) (JJ brown) (NN fox))))"
	s2 = "(S (NP (DT The) (JJ quick) (JJ brown) (NN fox)))"
	s3 = "(DT The) (JJ quick) (JJ brown) (NN fox)"
	
	print getTopLevelTag(s)
	print getTopLevelTag(s2)
	print getTopLevelTag(s3)
	'''
	
	# testing isLeafLevel()
	'''
	s = "( (S (NP (DT The) (JJ quick) (JJ brown) (NN fox))))"
	s2 = "(S (NP (DT The) (JJ quick) (JJ brown) (NN fox)))"
	s3 = "(DT The) (JJ quick) (JJ brown) (NN fox)"
	s4 = "(NP (DT The) (JJ quick) (JJ brown) (NN fox))"
	
	print isLeafLevel(s)
	print isLeafLevel(s2)
	print isLeafLevel(s3)
	print isLeafLevel(s4)
	'''
	
	# testing stripOneLevel()
	s = "( (S (NP (NP (DT The) (JJ last) (NN type)) (PP (IN of) (NP (NN carrier) (NN protein))) (SBAR (IN that) (S (NP (PRP we)) (VP (VB discuss))))) (VP (VBZ is) (NP (NP (DT a) (NN family)) (PP (IN of) (NP (NN transport) (NNS ATPases))) (SBAR (WHNP (WDT that)) (S (VP (VBP are) (PP (IN of) (NP (JJ great) (JJ clinical) (NN importance,))) (SBAR (RB even) (IN though) (S (NP (NP (PRP$ their) (JJ normal) (NNS functions)) (PP (IN in) (NP (JJ eucaryotic) (NNS cells)))) (VP (VBP are) (ADVP (RB only)) (ADVP (RB just)) (VP (VBG beginning) (S (VP (TO to) (VP (VB be) (ADJP (JJ discovered.))))))))))))))) )"
	print stripOneLevel(s)
