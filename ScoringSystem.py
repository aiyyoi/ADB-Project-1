import heapq

# Input:
#	Document titles
#	Document descriptions
#	Document links
#	Document text
#	Relevance feedback
#
# Output:
#	One or Two terms to be added to query for next iteration

class ScoringSystem():

	def __init__(self,vectorSpace,alpha,beta,gamma):
		self.vectors = vectorSpace.createDocVectors()
		self.keys = vectorSpace.getInvFileKeys()
		self.numRel = vectorSpace.getNumRel()
		self.numNonRel = vectorSpace.getNumNonRel()
		self.alpha = alpha
		self.beta = beta
		self.gamma = gamma

	@staticmethod
	def addVectors(v1,v2):
		return [float(x1) + float(x2) for (x1,x2) in zip(v1,v2)]
	@staticmethod
	def subtractVectors(v1,v2):
		return [float(x1) - float(x2) for (x1, x2) in zip(v1, v2)]	

	@staticmethod
	def scalarMultiply(scalar,vector):
		return [float(x) * scalar for x in vector]
	
	def scoreRocchio(self):
		relDocVec = self.vectors["rel"]
		nonRelDocVec = self.vectors["nonRel"]
		queryVec = self.vectors["queryWeights"]

		temp1 = self.scalarMultiply(self.alpha,queryVec)	
		temp2 = self.scalarMultiply(self.beta,relDocVec)
		temp2 = self.scalarMultiply(1/float(self.numRel),relDocVec)
		temp3 = self.scalarMultiply(self.gamma,nonRelDocVec)
		temp3 = self.scalarMultiply(1/float(self.numNonRel),nonRelDocVec)
		temp4 = self.subtractVectors(temp2,temp3)
		return self.addVectors(temp1,temp4)
	
	def getNewQuery(self):
		newQuery = self.scoreRocchio()
		oldQuery = self.vectors["queryWeights"]
		
		for i in range(len(oldQuery)):
			if(oldQuery[i] != 0):
				newQuery[i] = 0

		terms = sorted(self.keys)
		max = heapq.nlargest(2,newQuery)
		print "Augment by new terms : {0}".format(terms[newQuery.index(max[0])])#,terms[newQuery.index(max[1])])	
		return terms[newQuery.index(max[0])]#+' '+terms[newQuery.index(max[1])]
