import xml.etree.ElementTree as etree

def readxml(file):
	tree = etree.parse(file)
	root = tree.getroot()
	sentences = root.find('sentences')
	slist = sentences.findall('sentence')
	doc = open('result/' + file.split('.')[0] + '.txt','w') 
	for sen in slist:
		doc.write(sen.text)
	doc.close()
	print('Processed ' + file + ' : ' + str(len(slist)) + ' sentences')

names=open("names.txt", "r")
file_names=names.read()
nm=file_names.split()
for f in nm:
	print(f)
	readxml(f)





