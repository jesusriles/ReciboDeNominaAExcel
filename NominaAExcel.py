from PyPDF2 import PdfReader # pip install PyPDF2

def readFromPDF():
	# read the information from the PDF
	reader = PdfReader("test.pdf")
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


def separateByWords(usefulLines):
	words = [] # [["001", "SUELDO", "38,889.01"], ...]
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

pdfInfo = readFromPDF()
lines = separateTextByLines(pdfInfo)
usefulLines = getUsefulLines(lines)
getValues = separateByWords(usefulLines)

for x in getValues:
	print(x)

''' 
References:
https://www.geeksforgeeks.org/working-with-pdf-files-in-python/
https://pypi.org/project/PyPDF2/
'''
