def remWord_Space(file_name):
    file = open(file_name,'r')
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
    file = open(file_name,'w')
    file.write(b)
    file.close()
    print(file_name,end=" ")
    print("file has been processed")

names = open("names_words.txt","r")
names_files = names.read().split()
for nm in names_files:
    remWord_Space(nm)
