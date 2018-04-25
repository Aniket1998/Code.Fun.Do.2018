def remWord_Space(file_name):
    file = open(file_name,'r')
    a = file.readlines()
    b = ''
    count = 0
    for i in a:
        if(len(a.split())>3):
            b = b + i
    file.close()
    file_out = file_name.split(".")[0] + "_updated" + file_name.split(".")[1]
    file = open(file_out,'w+')
    file.write(b)
    file.close()
    print(file_name,end=" ")
    print("file has been processed")

names = open("names_words.txt","r")
names_files = names.read().split()
for nm in names_files:
    remWord_Space(nm)
