import os
xml_files = filter(lambda x: x.endswith('.xml'), os.listdir('citations_summ'))


out = open("names"+".txt", "w")
for f in xml_files:
	out.write(f+" ")
