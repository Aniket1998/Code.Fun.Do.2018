def remDate_Space(file_name):
    file = open(file_name,'r')
    a = file.read()
    b = a.split("Dated:")[0]
    c = "".join(b.split("\n"))
    file.close()
    file = open(file_name,'w')
    file.write(c)
    file.close()
    print(file_name,end=" ")
    print("file has been processed")

names = open("names.txt","r")
names_files = names.read().split()
for nm in names_files:
    remDate_Space(nm)
