import urllib2
import urllib
import base64
import json
import argparse
import VectorSpaceClass
import ScoringSystem

bingUrlBase = 'https://api.datamarket.azure.com/Bing/Search/Web?'
bingParams = {'$top': '10', '$format': 'json'}
#save your own key as key.json under the save path as this script
with open('key.json') as key_file:
	data = json.load(key_file)
accountKey = data['accountKey']
# authentications
accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
headers = {'Authorization': 'Basic ' + accountKeyEnc}

############### Method for Each Search and Display top10 Results #####################
def SearchAndDisplay(bingParams, nRound):
	print '='*15+ '\nRound '+str(nRound)
	#search and display flow
	bingUrl = bingUrlBase+urllib.urlencode(bingParams)
	print 'Query\t= '+ bingParams['Query']
	print 'Precision\t= '+ str(precision)
	print 'URL: '+bingUrl
	req = urllib2.Request(bingUrl, headers = headers)
	response = urllib2.urlopen(req)
	# decode response string to JSON format
	content = json.loads(response.read())
	#content contains the xml/json response from Bing. 
	i = 1
	feedbackList = []
	print 'Total no. of results : 10'
	print 'Bing Search Results: \n'+ '='*15
	for eachResult in content['d']['results']:
		print '\nResult '+str(i)+":"
		print "[\n Title: "+eachResult['Title']
		print ' URL: '+eachResult['DisplayUrl']
		print ' Summary: '+eachResult['Description']+'\n]'
		i += 1
		TakeFeedback(eachResult, feedbackList)
	CalculateAndDecide(feedbackList, nRound)
	#return content['d']['results']

################ Take Feedback #######################################################
def TakeFeedback(result, feedbackList):
	user_input = raw_input('Relevant (Y/N)? ').lower()
	if user_input == 'y':
		result['Relevant'] = 'y'
		feedbackList.append(result)
	if user_input == 'n':
		result['Relevant'] = 'n'
		feedbackList.append(result)
	if user_input != 'y' and user_input != 'n':
		print 'Wrong input'
		TakeFeedback(result, feedbackList)

################ Calculate Current Round Precision and Choose Path ###################
def CalculateAndDecide(feedbackList, nRound):
	items = 0
	for each in feedbackList:
		if each['Relevant'] == 'y':
			items += 1
	cur_precision = float(items)/10.0
	print '\n'+ '='*15
	print 'FEEDBACK SUMMARY\n'+ 'Query: '+ bingParams['Query']+ '\nCurrent Precision: '+ str(cur_precision)
	if (cur_precision > 0.0 and cur_precision < float(precision)):
		print 'Still blow the desired precision'
		AnalyzeAndModify(feedbackList, nRound+1)
	elif cur_precision == 0.0:
		print 'Precision at 0, unable to proceed'
		exit()
	else:
		print 'Desired precision reached: '+ str(cur_precision)
		exit()

###############  User Feedback and Modify Search Query    ############################
def AnalyzeAndModify(relatedList, nRound): # might need bingParams as input
	# Score, Rate and get those query keywords

	v = VectorSpaceClass.VectorSpace(relatedList,bingParams['Query'].strip("'"))
	rocchio = ScoringSystem.ScoringSystem(v, 1, 0.8, 0.3)
	new_words = rocchio.getNewQuery()
	# for eachTerm in v.invFile:
	# 	print eachTerm + ': idf-'+ str(v.invFile[eachTerm].idf)
	# 	for eachDoc in v.invFile[eachTerm].doc_tf_dict:
	# 		print '   docID-'+eachDoc+ ' -locations-'+str(v.invFile[eachTerm].doc_tf_dict[eachDoc])

	bingParams['Query'] = "'"+bingParams['Query'].strip("'")+ ' '+new_words+"'"
	SearchAndDisplay(bingParams, nRound)


#################### New Search and Feedback Session #################################
parser = argparse.ArgumentParser(prog='ADB Project 1', description = 'how to use the script')
parser.add_argument('-q', help = 'Single quoted search query', required = True)
parser.add_argument('-p', help = 'Precision @10, a number from 0 to 1', required = True)
args = parser.parse_args()

query = args.q
precision = args.p
bingParams['Query'] = "'"+query+"'"
SearchAndDisplay(bingParams, 1)

