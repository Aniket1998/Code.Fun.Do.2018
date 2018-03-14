from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import urllib.request as urllib2
import json
from gensim.summarization import summarize
# Create your views here.
def testview(request):
	context = {
		'page_title' : 'Legal Case Studies',
	}
	template = loader.get_template('legal/startpage.html')
	return HttpResponse(template.render(context,request))


def responseview(request):
	filetext = request.FILES['myfile'].read().decode('utf-8')
	impwords = callapi(filetext)
	name = request.FILES['myfile'].name.split('.')[0]
	context = {
		'filename' : request.FILES['myfile'].name.split('.')[0],
		'realtext' : preprocess(filetext,impwords),
		'summary' :  preprocess(summarize(filetext,word_count = len(filetext.split(' ')) * 0.2),impwords),
		'title' : ''
	}
	template = loader.get_template('legal/index.html')
	return HttpResponse(template.render(context,request))


def callapi(filetext):
	data =  {
		"Inputs": {
				"input1":
				{
					"ColumnNames": ["1", "2", "Column 2"],
					"Values": [ [ "0", "0", filetext ], [ "0", "0", filetext ], ]
				},        },
				"GlobalParameters": {
		}
	}

	body = str.encode(json.dumps(data))

	url = 'https://ussouthcentral.services.azureml.net/workspaces/8423fe6354e64c5583076f21aa2f23c0/services/0c172734030249a9865bc7ba4e95351f/execute?api-version=2.0&details=true'
	api_key = '1I5Pdv19ADalbWoDfKO7/yhnGL4bgdymg0RUopI+cQGgh0P6/C0C8JB5kA0GKNudTj4tc4UAGrn5OQ15Pf1oiw=='
	headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
	req = urllib2.Request(url, body, headers) 

	try:
		response = urllib2.urlopen(req)

		result = json.loads(response.read())
		return result['Results']['output1']['value']['Values'][0][0] 
	except urllib2.HTTPError as error:
		raise Http404("The document failed to comprehend with status code: " + str(error.code))                 


def preprocess(filetext,impwords):
	catchphrases = impwords.split(',')
	data = filetext.replace('\n','<br>')
	for word in catchphrases:
		if len(word.split(' ')) > 2:
			data = data.replace(word,'<b><i>' + word + '</b></i>')
	return data
