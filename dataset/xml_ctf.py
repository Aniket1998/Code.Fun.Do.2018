import xml.etree.ElementTree as etree

def readxml(file):
	tree = etree.parse(file)
	root = tree.getroot()
	sentences = root.find('catchphrases')
	slist = sentences.findall('catchphrase')
	doc = open('catchphrases/' + file.split('.')[0] + '.txt','w') 
	for sen in slist:
		doc.write(sen.text + '\n')
	doc.close()
	print('Processed ' + file + ' : ' + str(len(slist)) + ' catchphrases')

names=open("names.txt", "r")
file_names=names.read()
nm=file_names.split()
for f in nm:
	print(f)
	readxml(f)





