""" A class to convert a corpus of PREPROCESSED documents into the Vector Space representation """

from collections import defaultdict
import TermParamsClass
import math

class VectorSpace:
		
	N = 10 #Total number of documents in the corpus

	@staticmethod
	def computeTermFreq(rawFreq):
		return rawFreq

	@staticmethod
	def computeInverseDocFreq(numDocsWithTerm, numDocsTotal):
		return math.log(float(numDocsWithTerm) / numDocsTotal)

	def __init__(self,docs):
		self.vocab = set([]) #Build vocalbulary from title and text of all documents
		for d in docs:#["d"]["results"]:
			d["Title"] = d["Title"].split()
			d["Description"] = d["Description"].split()
			self.vocab.update(d["Title"])
			self.vocab.update(d["Description"])

		stopWords = set([])
                file = open("resources/english",'r').readlines()
                for i in range(len(file)):
                        stopWords.update(file[i].strip('\n'))
		self.vocab = self.vocab - stopWords

		#Insert Document-tf pairs into the inverted file
		self.invFile = defaultdict(TermParamsClass.TermParams)
		for v in self.vocab:
			temp = {};
			for d in docs:#["d"]["results"]:
				tCount = d["Title"].count(v) + d["Description"].count(v)
				tf= self.computeTermFreq(tCount)
				if tf != 0:
					temp[d["Url"]] = tf 

			print temp.keys()
			idf= self.computeInverseDocFreq(len(temp.keys()), self.N)
			self.invFile[v] = TermParamsClass.TermParams(idf,temp)

		

		
