class TermParams:
	
	def __init__(self,idf,doc_tf_dict):
		self.idf = idf;
		self.doc_tf_dict = doc_tf_dict;

	def getIdf(self):
		return self.idf

	def getDocs(self):
		return self.doc_tf_dict




