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
			return math.log(float(numDocsWithTerm) / numDocsTotal)
	@staticmethod
	def getAllIndices(list,term):
		return [i for i, x in enumerate(list) if x == term]

	def __init__(self,docs):
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
		for v in self.vocab:
			temp = {};
			for d in docs:		
				pos = self.getAllIndices(d["Title"] + d["Description"],v)
				if len(pos) != 0:	
					temp[d["DisplayUrl"]] = pos

			idf= self.computeInverseDocFreq(len(temp.keys()), self.N)
			self.invFile[v] = TermParamsClass.TermParams(idf,temp)

		

		
