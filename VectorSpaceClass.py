""" A class to convert a corpus of PREPROCESSED documents into the Vector Space representation """

from collections import defaultdict

class VectorSpace:
		
	N = 10 #Total number of documents in the corpus

	def computeTermFreq(rawFreq):
		return rawFreq

	def computerInverseDocFreq(numDocsWithTerm, numDocsTotal):
		return log(numDocsWithTerm / numDocsTotal)

	def __init__(self,docs):
		self.vocab = set([]) #Build vocalbulary from title and text of all documents
		for d in docs["d"]["results"]:
			d["Title"] = d["Title"].split()
			d["Description"] = d["Description"].split()
			vocab = vocab.union(d["Title"])
			vocab = vocab.union(d["Description"])

		#Insert Document-tf pairs into the inverted file
		self.invFile = defaultdict(dict)
		for v in vocab:
			for d in docs["d"]["results"]:
				tf= computeTermFreq(d["Title"].count(v) + d["Description"].count(v))
				if tf == 0:
					invFile[v][d["Url"]] = tf 
			idf= computeInverseDocFreq(len(invFile[v].keys()), self.N)
			invFile[v]["idf"] = idf

		

		
