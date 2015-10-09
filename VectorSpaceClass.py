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

	# Method to construct inverted file list
	def __init__(self,docs,origQuery):
		self.numRel = 0
		self.numNonRel = 0
		self.origQuery = origQuery.split()
		self.vocab = set([]) #Build vocalbulary from title and text of all documents
		for d in docs:	
			d["Title"] = d["Title"].split()
			d["Description"] = d["Description"].split()
			# to remove water mark like url keywords in titles and descriptions
			# as they are noises
			urlFilter = d['DisplayUrl'].partition('.')[2].partition('.')[0]
			d["Title"] = map(lambda s:s.strip('.,!()[]&"').lower(), d['Title'])
			d["Title"] = filter(lambda e: e!= urlFilter, d["Title"])
			d["Description"] = map(lambda s:s.strip('.,!()[]&"').lower(), d["Description"])
			d["Description"] = filter(lambda e:e!= urlFilter, d["Description"])
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
	def createDocVectors(self):#self,originalQuery):
		i = 0
		relWeights = [0 for i in range(len(self.invFile.keys()))]
		nonRelWeights = [0 for i in range(len(self.invFile.keys()))] 
		queryWeights = [0 for i in range(len(self.invFile.keys()))]	
		i = 0
		for key in sorted(self.invFile.keys()):
			currIdf = self.invFile[key].getIdf()
			queryWeights[i] = self.origQuery.count(self.invFile[key])*currIdf
			docs = self.invFile[key].getDocs()
			for d in docs.keys():
				if self.relevanceList[d] == 'y':
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

	def getInvFileKeys(self):
		return self.invFile.keys()	
