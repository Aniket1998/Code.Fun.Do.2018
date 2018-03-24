import re
import sys
import os

filename = sys.argv[1]
file = open(filename,"r")

regex = r"[^\.]+\d{1,2}\s\D{3,8}\s\d{2,4}\."

test_str = file.read()

matches = re.finditer(regex, test_str)

for matchNum, match in enumerate(matches):
    matchNum = matchNum + 1
    
    print ("{match}".format(match = match.group()))