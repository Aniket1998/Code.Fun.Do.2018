import re
import sys
import os

filename = sys.argv[1]
file = open(filename,"r")

regex = r"([A-Z][^\.!?]*)(\d{1,2}[t][h]\s\D{3,8}[,]\s\d{2,4}|\d{0,1}[1][s][t]\s\D{3,8}[,]\s\d{2,4}|\d{0,1}[2][n][d]\s\D{3,8}[,]\s\d{2,4}|\d{0,1}[3][r][d]\s\D{3,8}[,]\s\d{2,4}|\d{1,2}\s\D{3,8}[,]\s\d{2,4})\s([a-z][^\.!?]*)([\.!?])"

test_str = file.read()

matches = re.finditer(regex, test_str)

for matchNum, match in enumerate(matches):
    matchNum = matchNum + 1
    
    print ("{match}".format(match = match.group()))