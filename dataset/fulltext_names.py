import os
files = filter(lambda x: x.endswith('_words.txt'), os.listdir('sentences'))


out = open("names_words"+".txt", "w+")
for f in files:
	out.write(f+" ")
