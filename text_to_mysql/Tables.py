import TreeNode # self-written
import TreeSentenceFunctions

class SentencePhraseTableEntry:
	
	def __init__(self, tag, text):
		self.tag = tag # string
		self.text = text # string; empty string when the entry corresponds to a non-leaf tree node
		
	def getText(self):
		return self.text
	
	def getTag(self):
		return self.tag
	
	def __str__(self):
		return str((self.tag,self.text))


class SentencePhraseRelTableEntry:
	
	def __init__(self, objEntry, targetEntry, vertLvl, horiLvl):
		self.objEntry = objEntry # SentencePhraseTableEntry
		self.targetEntry = targetEntry # SentencePhraseTableEntry
		self.vertLvl = vertLvl # int
		self.horiLvl = horiLvl # int
	
	def getObjEntry(self):
		return self.objEntry

	def getTargetEntry(self):
		return self.targetEntry
		
	def getVertLvl(self):
		return self.vertLvl
		
	def getHoriLvl(self):
		return self.horiLvl
	
	def __str__(self):
		return str((str(self.objEntry),str(self.targetEntry),self.vertLvl,self.horiLvl))
