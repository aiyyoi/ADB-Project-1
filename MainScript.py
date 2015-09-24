import urllib2
import base64
import json

bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27gates%27&$top=10&$format=json'
#save your own key as key.json under the save path as this script
with open('key.json') as key_file:
	data = json.load(key_file)
accountKey = data['accountKey']

# authentications
accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
headers = {'Authorization': 'Basic ' + accountKeyEnc}


#search and display flow
req = urllib2.Request(bingUrl, headers = headers)
response = urllib2.urlopen(req)
# decode response string to JSON format
content = json.loads(response.read())
#content contains the xml/json response from Bing. 
print content['d']['results']