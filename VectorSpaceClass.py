""" A class to convert a corpus of PREPROCESSED documents into the Vector Space representation """

from collections import defaultdict
import TermParamsClass
import math

class VectorSpace:
		
	N = 10 #Total number of documents in the corpus

	@staticmethod
	def computeInverseDocFreq(numDocsWithTerm, numDocsTotal):
		if numDocsWithTerm == 0:
			return 0
		else:
			return -math.log(float(numDocsWithTerm) / numDocsTotal)
	@staticmethod
	def getAllIndices(list,term):
		return [i for i, x in enumerate(list) if x == term]

	def __init__(self,docs,origQuery):
		self.numRel = 0
		self.numNonRel = 0
		self.origQuery = origQuery.split()
		self.vocab = set([]) #Build vocalbulary from title and text of all relevant documents
		for d in docs:	
			d["Title"] = d["Title"].split()
			d["Description"] = d["Description"].split()
			d["Title"] = map(lambda s:s.strip('.,!()[]&"').lower(), d['Title'])
			d["Description"] = map(lambda s:s.strip('.,!()[]&"').lower(), d["Description"])
			self.vocab.update(d["Title"])
			self.vocab.update(d["Description"])

		# Construct the set for stopwords
		stopWords = []
	        file = open("resources/english",'r').readlines()
	        for i in range(len(file)):
	                stopWords.append(file[i].rstrip())

		# Take out stop words from current vocabulary set
		self.vocab = self.vocab - set(stopWords)

		#Insert Document-tf pairs into the inverted file
		self.invFile = defaultdict(TermParamsClass.TermParams)
		self.relevanceList = {}
		for v in self.vocab:
			temp = {};
			for d in docs:
				self.relevanceList[d["DisplayUrl"]] = d["Relevant"]		
				pos = self.getAllIndices(d["Title"] + d["Description"],v)
				if len(pos) != 0:	
					temp[d["DisplayUrl"]] = pos

			idf= self.computeInverseDocFreq(len(temp.keys()), self.N)
			self.invFile[v] = TermParamsClass.TermParams(idf,temp)

		

	#Function to create weight vectors for the relevant docs, non-relevant docs as well as the current query
	def createDocVectors(self,originalQuery):
		i = 0
		relWeights = [0 for i in range(len(self.invFile.keys()))]
		nonRelWeights = [0 for i in range(len(self.invFile.keys()))] 
		queryWeights = [0 for i in range(len(self.invFile.keys()))]	
		for key in sorted(self.invFile.keys()):
			currIdf = self.invFile[key].getIdf()
			queryWeights[i] = self.origQuery.count(self.invFile[key])*currIdf
			docs = self.invFile[key].getDocs()
			for d in docs.keys():
				if d["Relevant"] == 'y':
					self.numRel = self.numRel + 1; 
					relWeights[i] += len(docs[d])*currIdf
				else:
					self.numNonRel = self.numNonRel + 1
					nonRelWeights[i] += len(docs[d])*currIdf

			i = i+1

		return {"rel":relWeights,"nonRel":nonRelWeights,"queryWeights":queryWeights}						
			
	
	def getNumRel(self):
		return self.numRel

	def getNumNonRel(self):
		return self.numNonRel			

	def getInvFileKeys():
		return self.invFile.keys()	
