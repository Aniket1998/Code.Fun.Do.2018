import os
files = filter(lambda x: x.endswith('.txt'), os.listdir('sentences'))


out = open("names"+".txt", "w")
for f in files:
	out.write(f+" ")
