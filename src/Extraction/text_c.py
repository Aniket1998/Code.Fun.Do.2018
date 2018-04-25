import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
from time import time
import os

def load_data():
	categories=[]
	data=[]
	data_x=[]
	data_y=[]
	count=0
	for i in categories:
		count=count+1
		print(i,count)
		path="~/data_c/"+i+"/"
		names=os.listdir(path)
		for j in names:
			text_file=open(path+""+j)
			text=text_file.read()
			data_x.append(text)
			data_y.append(count)
			text_file.close()
			print(j)
	data.append(data_x)
	data.append(data_y)
	return data

data=load_data()

vectorizer = HashingVectorizer(stop_words='english', alternate_sign=False,n_features=2**16)
x = vectorizer.transform(data[0])
y = data[1]

naiv=MultinomialNB(alpha=0.01)
t0=time()
print(t0)
naiv.fit(x,y)
t_time=time()-t0
print(t_time)

naiv.predict(x[1])

pickle.dump(naiv,open("naive.sav","wb"))
