import TreeSentenceFunctions #self-written
import Tables # self-written

'''
TreeNode with no word (self.word == None) means that it's a phrase tag

For now, punctuations are not taken out for the sake of reconstructing the sentence from the database.
For example, "The dog is red." will be stored as the words "The", "dog", "is", "red." 
'''

#TODO:
'''
add instance var punctuation and take care of each case
', ; . ? !      '' "" ()'

Ignore (upper/lower) cases
'''

class TreeNode():

	punctuations = [',',';','.','?','!']

	def __init__(self,tag=None,word=None,hori=None,vert=None):
		self.tag = tag	# string
		self.word = word	# string
		#self.punctuation = punc # string; ', ; . ? !       "" ()'
		self.horizontal = hori # int
		self.vertical = vert # int
		self.children = [] # list of TreeNodes
	
	@staticmethod
	def treeStringToTree(treeString):
		topLevelTag = TreeSentenceFunctions.getTopLevelTag(treeString)
		root = TreeNode(tag=topLevelTag,hori=0,vert=0)
		root.reconstructTree(TreeSentenceFunctions.stripOneLevel(treeString))
		return root
	
	def reconstructTree(self,treeString):
		
		wordLst = TreeSentenceFunctions.splitPhrases(treeString)

		for phrase in wordLst:
			if TreeSentenceFunctions.isLeafLevel(phrase): # base case
				decomposedTuple = TreeSentenceFunctions.decomposePhrase(phrase)
				tag = decomposedTuple[0]
				word = decomposedTuple[1]
				#if word[-1] in TreeNode.punctuations:
					#word = word[:-1]
				childNode = TreeNode(tag,word,len(self.children),(self.vertical + 1))
				self.children.append(childNode)
			else:
				topLevelTag = TreeSentenceFunctions.getTopLevelTag(phrase)
				childNode = TreeNode(topLevelTag, None, len(self.children), (self.vertical + 1))
				self.children.append(childNode) 
				childNode.reconstructTree(TreeSentenceFunctions.stripOneLevel(phrase))  
	

	def toTreeString(self):
		s = self.toTreeStringHelper()
		return s[:-1] + ' ' + s[-1]
	
	def toTreeStringHelper(self):
		if self.isLeaf(): # at word level
			treeString = '(' + self.tag + ' ' + self.word + ')'
		else:
			treeString = '(' + self.tag 
			for child in self.children:
				treeString += ' ' + child.toTreeStringHelper() 
			
			treeString += ')'
			
		return treeString
			
	def isLeaf(self):
		return len(self.children) == 0

	def toSentence(self):
		#return self.toSentenceHelper()[:-1] + '.'
		return self.toSentenceHelper()[:-1]

	def toSentenceHelper(self):
		if self.isLeaf():
			return self.word + ' '
		else:
			sentence = ''
			for child in self.children:
				sentence += child.toSentenceHelper()
			
			return sentence
	
	def toTagWordTuple(self):
		return self.toTagWordTupleHelper()[:-1]
		
	def toTagWordTupleHelper(self):
		if self.isLeaf():
			return "(%s %s) " % (self.tag, self.word)
		else:
			sentence = ''
			for child in self.children:
				sentence += child.toTagWordTupleHelper()
			
			return sentence

	# mostly for debugging purposes
	def BFTraversal(self):
		queue = []
		queue.append(self)
		
		while len(queue) != 0:
			
			# dequeue
			node = queue[0]
			del queue[0]
			
			# visit node
			if node.word == None:
				print (node.tag, node.vertical, node.horizontal)
			else:
				print (node.tag, node.word, node.vertical, node.horizontal)
			
			# enqueue if any
			if not node.isLeaf():
				for child in node.children:
					queue.append(child)

	# return a list of SentencePhraseTableEntries
	def toLstOfSentencePhraseTableEntries(self):
		entries = []
		
		queue = []
		queue.append(self)
		
		while len(queue) != 0:
			
			# dequeue
			node = queue[0]
			del queue[0]
			
			#visit node
			if len(node.children) != 0: # node content is at phrase level/ non-leaf node
				entries.append(Tables.SentencePhraseTableEntry(node.tag,''))
			else: # node content is at word level (leaf)
				entries.append(Tables.SentencePhraseTableEntry(node.tag,node.word))
				
			# enqueue if any
			if not node.isLeaf():
				for child in node.children:
					queue.append(child)

		return entries

	# return a list of SentencePhraseRelTableEntries
	def toLstOfSentencePhraseRelTableEntries(self):
		entries = []
		
		queue = [] 
		queue.append(self)
		
		while len(queue) != 0:
			
			# dequeue
			node = queue[0]
			del queue[0]
			
			#visit node
			if len(node.children) != 0: # non-leaf node
				nodeWord = node.word
				if nodeWord == None:
					nodeWord = ''
				objEntry = Tables.SentencePhraseTableEntry(node.tag, nodeWord)
				for childNode in node.children:
					childNodeWord = childNode.word
					if childNodeWord == None:
						childNodeWord = ''
					targetEntry = Tables.SentencePhraseTableEntry(childNode.tag,childNodeWord)
					entries.append(Tables.SentencePhraseRelTableEntry(objEntry,targetEntry, node.vertical, node.horizontal))
				
			

			# enqueue if any
			if not node.isLeaf():
				for child in node.children:
					queue.append(child)


		return entries

### test cases
if __name__ == "__main__":		

	'''
	print 
	#treeString = "( (S (NP (DT The) (JJ quick) (JJ brown) (NN fox)) (VP (VBZ jumps) (PP (IN over) (NP (DT the) (JJ lazy) (NN dog))))) )"
	
	treeString = "( (S (NP (DT The) (JJ quick) (JJ brown) (NN fox))))"
	treeRoot = TreeNode.treeStringToTree(treeString)
	print treeRoot.toTreeString()
	#print treeString == treeRoot.toTreeString()
	
	#treeRoot.printTree()
	#treeRoot.BFSTraversal()
	print treeRoot.toSentence()
	print
	'''
	
	'''
	treeString = "( (S (NP (NP (DT The) (JJ last) (NN type)) (PP (IN of) (NP (NN carrier) (NN protein))) (SBAR (IN that) (S (NP (PRP we)) (VP (VB discuss))))) (VP (VBZ is) (NP (NP (DT a) (NN family)) (PP (IN of) (NP (NN transport) (NNS ATPases))) (SBAR (WHNP (WDT that)) (S (VP (VBP are) (PP (IN of) (NP (JJ great) (JJ clinical) (NN importance,))) (SBAR (RB even) (IN though) (S (NP (NP (PRP$ their) (JJ normal) (NNS functions)) (PP (IN in) (NP (JJ eucaryotic) (NNS cells)))) (VP (VBP are) (ADVP (RB only)) (ADVP (RB just)) (VP (VBG beginning) (S (VP (TO to) (VP (VB be) (ADJP (JJ discovered.))))))))))))))) )"
	sentence = "The last type of carrier protein that we discuss is a family of transport ATPases that are of great clinical importance, even though their normal functions in eucaryotic cells are only just beginning to be discovered."
	
	treeRoot = TreeNode.treeStringToTree(treeString)
	print treeRoot.toTreeString()
	print treeRoot.toTreeString() == treeString
	print treeRoot.toSentence() == sentence
	'''
	
	treeString = "( (S (NP (NP (DT The) (JJ last) (NN type)) (PP (IN of) (NP (NN carrier) (NN protein))) (SBAR (IN that) (S (NP (PRP we)) (VP (VB discuss))))) (VP (VBZ is) (NP (NP (DT a) (NN family)) (PP (IN of) (NP (NN transport) (NNS ATPases))) (SBAR (WHNP (WDT that)) (S (VP (VBP are) (PP (IN of) (NP (JJ great) (JJ clinical) (NN importance,))) (SBAR (RB even) (IN though) (S (NP (NP (PRP$ their) (JJ normal) (NNS functions)) (PP (IN in) (NP (JJ eucaryotic) (NNS cells)))) (VP (VBP are) (ADVP (RB only)) (ADVP (RB just)) (VP (VBG beginning) (S (VP (TO to) (VP (VB be) (ADJP (JJ discovered.))))))))))))))) )"
	treeRoot = TreeNode.treeStringToTree(treeString)
	#print TreeSentenceFunctions.splitPhrases(treeRoot.toTagWordTuple())
	entries = treeRoot.toLstOfSentencePhraseRelTableEntries()
	for entry in entries:
		print entry
	
