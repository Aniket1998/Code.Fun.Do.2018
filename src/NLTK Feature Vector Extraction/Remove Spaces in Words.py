def remWord_Space(file_name):
    file = open('06_11_words.txt','r')
    a = file.read()
    b = ''
    count = 0
    for i in a:
    	if(i!='\n'):
    		count = 0
    		b += i
    		continue
    	if(count==0):
    		b += i
    		if(i=='\n'):
    			count = 1
    file.close()
    file = open('06_11_words_2.txt','w')
    file.write(b)
    file.close()

remWord_Space('a')