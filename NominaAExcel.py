import sys
from PyPDF2 import PdfReader # pip install PyPDF2

FILENAME = sys.argv[1]

def readFromPDF():
	# read the information from the PDF
	reader = PdfReader(FILENAME)
	number_of_pages = len(reader.pages)

	# should only have 1 page
	if(number_of_pages > 1):
		print("[-] There is more than 1 page!")
		exit()

	page = reader.pages[0]
	text = page.extract_text()
	return text


'''
	- input: all text from the PDF
	- return: a list with every line of the PDF (correctly separated by line)
'''
def separateTextByLines(text):
	listWithLines = []

	# print line by line
	string = ''
	for line in text:
		string += line

		if(line == '\n'):
			listWithLines.append(string)
			string = ''

	return listWithLines


'''
	- input: separateTextByLines()
	- output: a list with only the lines I need
'''
def getUsefulLines(lines):
	# identify the line that contain "Concepto Importe" and "Recibí de la empresa arriba mencionada"
	# all information we need is between those lines

	usefulInformation = []
	appendInformation = False

	for line in lines:
		if "Concepto Importe" in line:
			appendInformation = True
			continue

		if "Recibí de la empresa arriba mencionada" in line:
			usefulInformation.append(line) # we need this line because at the beggining it have a number we need to split
			break

		if(appendInformation):
			usefulInformation.append(line)

	return usefulInformation


'''
	- input: getUsefulLines(lines) - the lines that we need to process
	- output: split the lines/sentences by spaces
'''
def separateBySpaces(usefulLines):
	words = []
	s = ''

	for line in usefulLines:
		for letter in line:
			if(letter != " "):
				if(letter == '\n'):
					break
				s += letter
			else:
				words.append(s)
				s = ''

	return words


'''
	- input: All the words/strings
	- output: 
		Split and categorize the words in (1) Concept Id, (2) Concept name, (3) Numbers and return a list
		with all the information organized
		E.g. of output [ [001, SUELDO, 100,889.01], [002, TEST, 1,889.99] ] 
'''
def mapTheInformationInStructure(words):
	
	infoStructured = []
	tmpList = [] # [Concept Id, Concept, Number] e.g. [001, SUELDO, 100,889.01]

	for word in words:

		if(len(word) == 0): # if it is an empty line, ignore it
			continue

		# Concept Id
		if(len(tmpList) == 0 and len(word) <= 4 and word[0].isnumeric()):
			tmpList.append(word)
			continue

		# Concept name
		if(not word[0].isnumeric()):
			
			if(len(tmpList) == 1):
				tmpList.append(word)
			else:
				try:
					tmpList[1] += " " + word
				except IndexError:
					pass
			continue

		if(word[0].isnumeric() and "." in word): # Number
			
			if(splitIfMoreThan2Decimals(word)):
				word1,word2 = splitWordsAfter2Decimals(word)
				tmpList.append(word1)
				if(len(tmpList) != 1): # don't add to the final list if it's only one number
					infoStructured.append(tmpList)
				tmpList = []
				tmpList.append(word2)
				continue

			tmpList.append(word)

			if(len(tmpList) != 1): # don't add to the final list if it's only one number
				infoStructured.append(tmpList)
			tmpList = []
			continue

	return infoStructured


def splitIfMoreThan2Decimals(word):
	charsAfterDot = 0
	afterDot = False

	for char in word:
		if(char == "."):
			afterDot = True
			continue

		if(afterDot):
			charsAfterDot+=1

	if(charsAfterDot > 2):
		return True
	return False


def splitWordsAfter2Decimals(word):
	dotAt = word.index(".") + 3
	return word[:dotAt], word[dotAt:]

pdfInfo = readFromPDF()
lines = separateTextByLines(pdfInfo)
usefulLines = getUsefulLines(lines)
words = separateBySpaces(usefulLines)
informationStructured = mapTheInformationInStructure(words)

for x in informationStructured:
	print(x)

''' 
References:
https://www.geeksforgeeks.org/working-with-pdf-files-in-python/
https://pypi.org/project/PyPDF2/
'''
