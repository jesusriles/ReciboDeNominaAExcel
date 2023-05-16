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
	- output: a list of hashes (key-value) with the information that needs to be extracted (e.g. {001 SUELDO => 38,889.012}, {258 GASTOS MEDICOS => 453.00})
'''
def getUsefulLines(lines):
	# identify the line that contain "Concepto Importe" and "NETO A PAGAR"
	# all information we need is between those lines

	usefulInformation = []
	appendInformation = False

	for line in lines:
		if "Concepto Importe" in line:
			appendInformation = True

		if "NETO A PAGAR" in line:
			break

		if(appendInformation):
			usefulInformation.append(line)

	del usefulInformation[0] # delete line "Concepto Importe Concepto Importe"
	return usefulInformation

''' ---------------------------------------------------------- '''

pdfInfo = readFromPDF()
lines = separateTextByLines(pdfInfo)
usefulLines = getUsefulLines(lines)


for x in usefulLines:
	print(x)

''' 
References:
https://www.geeksforgeeks.org/working-with-pdf-files-in-python/
https://pypi.org/project/PyPDF2/
'''
