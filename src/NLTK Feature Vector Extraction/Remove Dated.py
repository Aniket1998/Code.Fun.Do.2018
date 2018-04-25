def remDate_Space(file_name):
    file = open('data.txt','r')
    a = file.read()
    b = a.split("Dated:")[0]
    c = "".join(b.split("\n"))
    file.close()
    file = open('data.txt','w')
    file.write(c)
    file.close()
