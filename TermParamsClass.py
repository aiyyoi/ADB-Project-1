'''
	Utility class for parameters of each term in inverted file list
	idf: inverse documents frequency
	doc_tf_dict: for each term, the dictionary indexed by docID, 
					with array of occurrence locations of the term in docID as value
'''
class TermParams:
	
	def __init__(self,idf,doc_tf_dict):
		self.idf = idf;
		self.doc_tf_dict = doc_tf_dict;

	def getIdf(self):
		return self.idf

	def getDocs(self):
		return self.doc_tf_dict




