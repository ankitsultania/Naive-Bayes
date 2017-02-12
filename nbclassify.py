import os
import sys
import string
import math
import re

path_testdata = sys.argv[-1]
_POSITIVE_ = 0
_NEGATIVE_ = 1
_DECPETIVE_ = 2
_TRUTHFUL_ = 3

def WriteOutput(decptrustr, posnegstr, file, fp):
	fp.write(decptrustr + " " + posnegstr + " " + file +"\n")

def CreateOutputFile():
	f = open("nboutput.txt", "w")
	return(f)

def ComputeMAP(tokenlist, tokensdict, classRef):
	cmap = 0.0
	cmap = math.log(tokensdict["prior"][classRef])
	for text in tokenlist:
		if text in tokensdict:
				cmap += math.log(tokensdict[text][classRef])
	return(cmap)

def IsPositiveOrNegative(tokenlist, tokensdict):
	poscmap = float(ComputeMAP(tokenlist, tokensdict, _POSITIVE_))
	negcmap = float(ComputeMAP(tokenlist, tokensdict, _NEGATIVE_))
	if negcmap > poscmap:
		return("Negative")
	else:
		return("Positive")
		
def IsTruthfulOrDeceptive(tokenlist, tokensdict):
	trucmap = float(ComputeMAP(tokenlist, tokensdict, _TRUTHFUL_))
	decpcmap = float(ComputeMAP(tokenlist, tokensdict, _DECPETIVE_))
	if decpcmap > trucmap:
		return("Decpetive")
	else:
		return("Truthful")
		
def ExtractTokensFromTest(filepath):
	wordlist = [""]
	with open(filepath, "r") as fp:
		for word in fp.read().split():
			term= "".join(c for c in word.lower() if c not in string.punctuation)
			term= re.sub( '[0-9]', '', term)
			if term != '' and term != ' ':
				wordlist.append(term)
	return(wordlist)

def Read_TestData(path):
	filelist = [""]
	for subdir, dirs, files in os.walk(path):
		for file in files:
			filepath = os.path.join(subdir, file)
			if ".txt" in filepath and "README.txt" not in filepath:
				#print filepath
				filelist.append(filepath)
				
	return filelist
		
def Parse_nbmodel(filename, sep):
    with open(filename, "r") as f:
        dict = {}
        for line in f:
            values = line.split(sep)
            dict[values[0]] = [float(values[1]), float(values[2]), float(values[3]), float(values[4])]
        return(dict)	

def AnalyzeData(filelist, tokensdict, fp):
	for filepath in filelist[1:]:
		testtokenlist = ExtractTokensFromTest(filepath)
		posnegstr = IsPositiveOrNegative(testtokenlist, tokensdict)
		decptrustr = IsTruthfulOrDeceptive(testtokenlist, tokensdict)
		WriteOutput(decptrustr, posnegstr, filepath, fp)
	

params = Parse_nbmodel("nbmodel.txt", " ")
fp = CreateOutputFile()
files = Read_TestData(path_testdata)
AnalyzeData(files, params, fp)
fp.close()
