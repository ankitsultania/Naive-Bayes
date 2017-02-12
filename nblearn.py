#Tokenizations is required to get a count of a token in a document in a class.
#Perform mutual information on all the tokens.
#Select subset of all the token based on a threshold by comparing mutual info values.
#Compute probabilities of selected features.
import os
import sys
import string
import re
import operator
import math

_POSITIVE_ = 0
_NEGATIVE_ = 1
_DECEPTIVE_ = 2
_TRUTHFUL_ = 3

classList = ['positive', 'negative', 'truthful', 'deceptive']
dict = {}
dop = {}
rootdir = sys.argv[-1]
print rootdir
totalDocx = 0
totalPosDocx = 0
totalNegDocx = 0
totalDecpDocx = 0
totalTruDocx = 0

def CalculateTotalTokens(d, classRef):
	totalTerms = 0
	for x in d.keys():
		totalTerms += d[x][classRef]
	return totalTerms

def ApplySmoothing(d, classRef):
	isRequired = False
	for x in d.keys():
		if d[x][classRef] == 0:
			isRequired = True
			break

	if isRequired == True:
		for x in d.keys():
			d[x][classRef] += 1
		return True
	else:
		return False
				
def Term_Classify(d, filepath, word):
	#Check for class of the term positive:0, negative:1, truthful:2, deceptive:3
	#Note if will belong to (positive or negative) and (truthful or deceptive)
	if "positive" in filepath:
		d[word][0]+=1
	elif "negative" in filepath:
		d[word][1]+=1
	if "deceptive" in filepath:
		d[word][2]+=1
	elif "truthful" in filepath:
		d[word][3]+=1
	
	d[word][4]+=1
			
def Add_Word_To_Dict(d,filepath, word):
	if d.__contains__(word):
		Term_Classify(d, filepath, word)
		
	else:
		d[word] = [0,0,0,0,0]
		Term_Classify(d, filepath, word)
	
def Tokenization(tokenizeFile):
	#Code to perform lower casing of each term and removing the punctuations
	#Read the tokens delimited by space.
	wordlistScanned = [""]
	with open(tokenizeFile) as reviewFile:
		for line in reviewFile:
			for word in line.split():
				tokenized_word = "".join(c for c in word.lower() if c not in string.punctuation)
				tokenized_word = re.sub( '[0-9]', '', tokenized_word)
				if tokenized_word != '' and tokenized_word != ' ':			
					Add_Word_To_Dict(dict, tokenizeFile, tokenized_word)
	
def tokenize():
	#Open files iteratively. Note: the folder name contains the class name.
	global totalDocx, totalPosDocx, totalNegDocx, totalDecpDocx, totalTruDocx
	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
			filepath = os.path.join(subdir, file)
			if ".txt" in filepath:
				totalDocx += 1
				if "positive" in filepath:
					totalPosDocx += 1
				elif "negative" in filepath:
					totalNegDocx += 1
				if "deceptive" in filepath:
					totalDecpDocx += 1
				elif "truthful" in filepath:
					totalTruDocx += 1
				Tokenization(filepath)

def writeDict(dict, filename, sep):
    with open(filename, "w") as f:
        for i in sorted(dict.keys()):            
            f.write(i + " " + sep.join([str(x) for x in dict[i]]) + "\n")
					
tokenize()
totalPosTokens = CalculateTotalTokens(dict, _POSITIVE_)
totalNegTokens = CalculateTotalTokens(dict, _NEGATIVE_)
totalDecpTokens = CalculateTotalTokens(dict, _DECEPTIVE_)
totalTruTokens = CalculateTotalTokens(dict, _TRUTHFUL_)

#print("Before smoothing")
#print(len(dict))
#print(totalPosTokens)
#print(totalNegTokens)
#print(totalDecpTokens)
#print(totalTruTokens)

if ApplySmoothing(dict, _POSITIVE_) == True:
	totalPosTokens += len(dict)
if ApplySmoothing(dict, _NEGATIVE_) == True:
	totalNegTokens += len(dict)
if ApplySmoothing(dict, _DECEPTIVE_) == True:
	totalDecpTokens += len(dict)
if ApplySmoothing(dict, _TRUTHFUL_) == True:
	totalTruTokens += len(dict)

#print(totalDocx)
#print(totalPosDocx)
#print(totalNegDocx)
#print(totalDecpDocx)
#print(totalTruDocx)

#for x in sorted(dictUnique.keys()):
	#if dictUnique[x][4] >=1280:
#		print x,'=',dictUnique[x]
#print("_________________________________")
#for x in sorted(dict.keys()):
#	if dict[x][4] >1000:
#		print x,'=',dict[x] 
#for it in sorted(dict.items(), key=lambda x: x[1], reverse = True):
#	print it, "\n"

#print("After smoothing")
#print(len(dict))
#print(totalPosTokens)
#print(totalNegTokens)
#print(totalDecpTokens)
#print(totalTruTokens)

for term in dict.keys():
	dop[term] = [dict[term][0]/float(totalPosTokens), dict[term][1]/float(totalNegTokens), dict[term][2]/float(totalDecpTokens), dict[term][3]/float(totalTruTokens)]
	
dop["prior"] = [totalPosDocx/float(totalDocx), totalNegDocx/float(totalDocx), totalDecpDocx/float(totalDocx), totalTruDocx/float(totalDocx)]

#for t in dop.keys():
#	print t,"=",dop[t]

#nbmodel = open("nbmodel.txt", "w")
#for token in sorted(dop.keys()):
	##if token != '' and token != ' ':
#		nbmodel.write(token)
#		nbmodel.write("=")
#		nbmodel.write(str(dop[token]))
#		nbmodel.write("\n")
#nbmodel.close()

writeDict(dop, "nbmodel.txt", " ")









