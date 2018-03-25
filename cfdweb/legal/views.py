from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.template import loader
import urllib.request as urllib2
import json
from gensim.summarization import summarize
# Create your views here.
abilities = "Brief you about the document<br>Describe it in a little more detail<br>Fetch you the important words in it<br>"
defaultmsg = "Hi! Have anything to ask about the document? I can<br>" + abilities
def testview(request):
	context = {
		'page_title' : 'Legal Case Studies',
		'readfile' : 'https://drive.google.com/file/d/1prRlrLEK6St6Lsp9O3FyUyc-A4a9KuUt/view'
	}
	template = loader.get_template('legal/startpage.html')
	return HttpResponse(template.render(context,request))

def readmeview(request):
	context = {
		'page_title' : 'Case Studies | Team DeepVaders',
		'readme' : 'https://drive.google.com/file/d/1prRlrLEK6St6Lsp9O3FyUyc-A4a9KuUt/view'
	}
	template = loader.get_template('legal/readme.html')
	return HttpResponse(template.render(context,request))


def responseview(request):
	if request.method != 'POST':
		raise Http404('Wrong url accessed. Access the main page or the readme')
	if 'myfile' not in request.FILES.keys():
		raise Http404('You have not uploaded the file. Please go to the main page and then upload a file in txt format')
	if request.FILES['myfile'].name.split('.')[1] != 'txt':
		raise Http404('The file is not in text format. Please upload the file in proper format')
	filetext = request.FILES['myfile'].read().decode('utf-8')
	impwords = callapi(filetext)
	name = request.FILES['myfile'].name.split('.')[0]
	summary = prepsummary(filetext)
	chatsummary = prepchatsummary(filetext)
	chatshortsummary = prepchatshortsummary(filetext)
	context = {
		'filename' : request.FILES['myfile'].name.split('.')[0],
		'realtext' : preprocess(filetext,impwords),
		'summary' :  preprocess(summary,impwords),
		'title' : 'Analysis of ' + request.FILES['myfile'].name.split('.')[0],
		'chatkeywords' : parsekeywords(impwords),
		'chatsummary' : preprocess(chatsummary,impwords),
		'chatshortsummary' : preprocess(chatshortsummary,impwords),
		'defaultmsg' : defaultmsg,
	}
	template = loader.get_template('legal/index.html')
	return HttpResponse(template.render(context,request))

def prepsummary(filetext):
	sum = summarize(filetext,word_count=len(filetext.split(' ')) * 0.2)
	if len(sum) < 1:
		sum = summarize(filetext,word_count=len(filetext.split(' ')) * 0.3)
	if len(sum) < 1:
		sum = summarize(filetext,word_count=len(filetext.split(' ')) * 0.4)
	if len(sum) < 1:
		sum = summarize(filetext,word_count=len(filetext.split(' ')) * 0.5)
	if len(sum) < 1:
		sum = 'Sorry, the document is too small to be summarised'
	return sum

def prepchatsummary(filetext):
	sum = summarize(filetext,word_count=len(filetext.split(' ')) * 0.1)
	if len(sum) < 1:
		sum = summarize(filetext,word_count=len(filetext.split(' ')) * 0.2)
	if len(sum) < 1:
		sum = summarize(filetext,word_count=len(filetext.split(' ')) * 0.3)
	if len(sum) < 1:
		sum = 'Sorry, the document is too small to be summarised further'
	return sum

def prepchatshortsummary(filetext):
	sum = summarize(filetext,word_count=len(filetext.split(' ')) * 0.05)
	if len(sum) < 1:
		sum = summarize(filetext,word_count=len(filetext.split(' ')) * 0.1)
	if len(sum) < 1:
		sum = 'Sorry, the document is too small to be summarised further'
	return sum

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

def parsekeywords(impwords):
	keyw = "<i>";
	ctf = impwords.split(',')
	for word in ctf:
		if len(word.split(' ')) > 2:
			keyw += word + "<br>"
	keyw += "</i>"
	return keyw