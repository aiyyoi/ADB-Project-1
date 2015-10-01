# Class with functions responsible for preprocessing text

class Preprocessor:

	""" Function to remove stop words as listed in the NLTK corpus.
	    Arguments:
		document: A dictionary with the keys title, desc and text and corresponding values as lists of strings
	"""
	@classmethod
	def deleteStopWords(document):	
		stopWords = []
		file = open("/resources/english",'r').readlines()
		for i in range(len(file)):
			stopWords.append(file[i].strip('\n'))
		
		title_new = [x for x in document["title"] if x not in stopWords]
		desc_new =  [x for x in document["desc"] if x not in stopWords]
		text_new = [x for x in document["text"] if x not in stopWords]

		return {'title':title_new, 'desc':desc_new, 'text':text_new}


