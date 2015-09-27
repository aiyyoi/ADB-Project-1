import urllib2
import urllib
import base64
import json
import argparse

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
def SearchAndDisplay(bingParams):
	#search and display flow
	bingUrl = bingUrlBase+urllib.urlencode(bingParams)
	print bingUrl
	req = urllib2.Request(bingUrl, headers = headers)
	response = urllib2.urlopen(req)
	# decode response string to JSON format
	content = json.loads(response.read())
	#content contains the xml/json response from Bing. 
	i = 1
	for eachResult in content['d']['results']:
		print str(i)+": "+eachResult['Title']+'\n'+eachResult['Url']+'\n'+eachResult['Description']+'\n'
		i += 1
	TakeFeedback(content['d']['results'])
	#return content['d']['results']

################ Take Feedback #######################################################
def TakeFeedback(resultList):
	user_input = raw_input('Tell us which is relevant by index: ').split()
	feedbackList = []
	for eachIndex in user_input:
		feedbackList.append(resultList[int(eachIndex)-1])
	CalculateAndDecide(feedbackList)

################ Calculate Current Round Precision and Choose Path ###################
def CalculateAndDecide(feedbackList):
	cur_precision = float(len(feedbackList))/10.0
	#print cur_precision == 0.0
	if (cur_precision > 0.0 and cur_precision < float(precision)):
		AnalyzeAndModify(feedbackList)
	elif cur_precision == 0.0:
		print 'Precision at 0, unable to proceed'
		exit()
	else:
		print 'Desired precision reached: '+ str(cur_precision)
		exit()

###############  User Feedback and Modify Search Query    ############################
def AnalyzeAndModify(relatedList): # might need bingParams as input
	# Score, Rate and get those query keywords
	#
	#
	bingParams['Query'] = "'new query for now'"
	SearchAndDisplay(bingParams)


#################### New Search and Feedback Session #################################
parser = argparse.ArgumentParser(prog='ADB Project 1', description = 'how to use the script')
parser.add_argument('-q', help = 'Single quoted search query', required = True)
parser.add_argument('-p', help = 'Precision @10, a number from 0 to 1', required = True)
args = parser.parse_args()

print('Initial Query and feedback session:')
query = args.q
precision = args.p
bingParams['Query'] = "'"+query+"'"
SearchAndDisplay(bingParams)





