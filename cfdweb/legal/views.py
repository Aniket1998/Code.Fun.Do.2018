from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.template import loader
import urllib.request as urllib2
import json
from gensim.summarization import summarize
import re
from django.contrib.staticfiles.templatetags.staticfiles import static

from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import requests

#NLTK specific imports
import numpy as np 
import nltk
from nltk.tokenize import word_tokenize
from nltk.chunk import conlltags2tree
from nltk.tree import Tree

# Create your views here.
abilities = "Brief you about the document<br>List the dated events<br>Point the important words in it<br>"
defaultmsg = "Hi! Have anything to ask about the document? I can<br>" + abilities
rawstart = "Hi! Have anything to ask about the document/n/nI can brief you about the document, list the dated events, point the important words in it"
categories = ['Appellate Tribunal For Electricity','Central Administrative Tribunal','Central Information Commission','Competition Commission of India','Income Tax Appellate Tribunal','Consumer Disputes Redressal', 'National Green Tribunal' ,'Company Law Board', 'Customs, Excise and Gold Tribunal' , 'Securities Appellate Tribunal']
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
	orgs,persons,locs = loadorgspersonslocs(filetext)
	impwords = callapi(filetext)
	name = request.FILES['myfile'].name.split('.')[0]
	summary = prepsummary(filetext)
	chatsummary = prepchatsummary(filetext)
	chatshortsummary = prepchatshortsummary(filetext)
	date_events = extractdates(filetext)
	context = {
		'filename' : request.FILES['myfile'].name.split('.')[0],
		'realtext' : preprocess(filetext,impwords),
		'summary' :  preprocess(summary,impwords),
		'title' : 'Analysis of ' + request.FILES['myfile'].name.split('.')[0],
		'chatkeywords' : parsekeywords(impwords),
		'chatsummary' : preprocess(chatsummary,impwords),
		'chatshortsummary' : preprocess(chatshortsummary,impwords),
		'defaultmsg' : defaultmsg,
		'rawstart' : rawstart,
		'rawchatsummary' : chatsummary,
		'rawchatshortsummary' : chatshortsummary,
		'rawchatkeywords' : impwords,
		'rawdates' : date_events,
		'chatdates' : date_events.replace('\n','<br>'),
		'category' : categories[get_category(filetext)],
		'orgs' : orgs,
		'persons' : persons,
		'locs' : locs,
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
	sum = summarize(filetext,word_count=len(filetext.split(' ')) * 0.01)
	if len(sum) < 1:
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

def extractdates(filetext):
	regex = r"([A-Z][^\.!?]*)(\d{1,2}[t][h]\s\D{3,8}[,]\s\d{2,4}|\d{0,1}[1][s][t]\s\D{3,8}[,]\s\d{2,4}|\d{0,1}[2][n][d]\s\D{3,8}[,]\s\d{2,4}|\d{0,1}[3][r][d]\s\D{3,8}[,]\s\d{2,4}|\d{1,2}\s\D{3,8}[,]\s\d{2,4})\s([a-z][^\.!?]*)([\.!?])"
	totalstr = ""
	matches = re.finditer(regex,filetext)
	for matchNum,match in enumerate(matches):
		totalstr += match.group()
	return totalstr


#change this URL before deploying
def get_category(filetext):
	r = requests.get(url = "http://localhost:8000/static/legal/naive.sav")
	naiv=pickle.loads(r.content,encoding='latin1')
	vectorizer = HashingVectorizer(stop_words='english', alternate_sign=False,n_features=2**16)
	categories=['aptels','cat','cic']
	r2 = requests.get(url = "http://localhost:8000/static/legal/eg.txt")
	test_data=[]
	test_data.append(filetext)
	test_data.append(r2.text)
	test = vectorizer.transform(test_data)
	k = naiv.predict(test)
	return k[0]-1

def process_text(txt_file):
    raw_text = txt_file
    token_text = word_tokenize(raw_text)
    return token_text

def nltk_tagger(token_text):
    tagged_words = nltk.pos_tag(token_text)
    clean_tags = []
    for (i,j) in tagged_words:
        if(j=='NN'):
            clean_tags.append((i,j))
    ne_tagged = nltk.ne_chunk(tagged_words)
    return(ne_tagged)

def structure_ne(ne_tree):
    ne = []
    for subtree in ne_tree:
        if type(subtree) == Tree: # If subtree is a noun chunk, i.e. NE != "O"
            ne_label = subtree.label()
            ne_string = " ".join([token for token, pos in subtree.leaves()])
            ne.append((ne_string, ne_label))
    return ne

def nltk_main(txt):
    return (structure_ne(nltk_tagger(process_text(txt))))

def get_tags(txt):
    ner_tags = nltk_main(txt)
    person = []
    orgs = []
    loc = []
    for (i,j) in ner_tags:
        if(j=='ORGANIZATION'):
            orgs.append(i)
        elif(j=='PERSON'):
            person.append(i)
        elif(j=='LOCATION' or j=='GPE'):
            loc.append(i)
    return (orgs,person,loc)

def clean_up(arr,c=20):
    if((len(arr)-len(set(arr)))/len(arr)>=0.8):
        return set(arr)
    else:
        freq = nltk.FreqDist(arr)
        arr_im = []
        if(c==0):
            for i in freq:
                if(freq[i]<=1):
                    if(len(i)>=8 and len(i)<=18):
                        arr_im.append(i)
            return set(arr_im)
        threshold = c * len(set(arr))/len(arr)
        for i in freq:
            if(freq[i]>=threshold):
                arr_im.append(i)
        return set(arr_im)

def run(txt):
    (o,p,l) = get_tags(txt)
    o = clean_up(o,c=20)
    p = clean_up(p,c=0)
    l = clean_up(l,c=5)
    return (list(o), list(p), list(l))

def loadorgspersonslocs(txt):
	orgstr = ""
	personstr = ""
	locstr = ""
	o,p,l = run(txt)
	for name in o:
		if name == 'Kanoon':
			pass
		else:
			orgstr = orgstr + name + ", "
	for name2 in l:
		if name2 == 'Kanoon':
			pass
		else:
			locstr = locstr + name2 + ", "
	for name3 in p:
		if name3 == 'Kanoon':
			pass
		else:
			personstr = personstr + name3 + ", "
	
	orgstr = orgstr[:-2]
	locstr = locstr[:-2]
	personstr = personstr[:-2]
	return orgstr,personstr,locstr