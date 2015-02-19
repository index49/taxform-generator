#!/usr/bin/python

from PyPDF2 import PdfFileWriter, PdfFileReader
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import random
import getTax
import sys
import csv
import json
import re
import array

def getScheduleA(inputData, d):
	a = [0.0] * 30
	a[2] = d[38]
	a[3] = a[2] * .10
	if a[3] < a[1]:
		a[4] = a[1] - a[3]
	a[5] = float(inputData['w2']['17'])
	a[6] = float(inputData['misc']['real_estate'])
	a[9] = sum(a[5:8+1])
	a[10] = float(inputData['misc']['mortgage_interest'])
	a[15] = sum(a[10:14+1])
	a[16] = float(inputData['misc']['gifts'])
	a[19] = sum(a[16:18+1])
	a[24] = sum(a[21:23+1])
	if a[26] < a[24]:
		a[27] = a[24]-a[26]
	if d[38] < 150000:
		a[29] = a[4] + a[9] + a[15] + a[19] + a[24] + a[27] + a[28]
	return a

def getTaxValues(inputData):

	w2 = inputData['w2']
	d = [0.0] * 80
	
	status = getTax.getStatus('sep')
	data = getTax.read_p505('p505.txt')
	
	d[7] = w2['1']
	d[8] = float(inputData['misc']['taxable_interest'])
	d[10] = float(inputData['misc']['taxable_refund'])
	d[22] = sum(d[7:21+1])			# total income 
	
	d[37] = d[22] - d[36]			# adjusted gross income 

	d[38] = d[37]
	schedA = getScheduleA(inputData, d)
	d[40] = schedA[29]
	d[41] = d[38] - d[40]
	d[42] = 3950					# exemptions

	d[43] = d[41] - d[42]
	d[44] = getTax.calcTax(data[status], d[43])
	d[47] = sum(d[44:46+1])

	d[56] = d[47] - d[55]
	d[60] = float(inputData['misc']['homebuyer_credit'])
	d[63] = sum(d[55:60+1])

	d[64] = w2['2']					# federal income tax witheld
	d[74] = sum(d[64:71+1])			# total payments

	if d[74] > d[63]:
		d[75] = d[74] - d[63]
		d[76] = d[75]
	else:
		d[77] = d[63] - d[74]

	return d

def initPage(can):
	can.setFont("Helvetica" , 10)
	can.setFillColorRGB(0,0,1)

def insertValue(can, values, index, x, y, ySpace):
	val = values[index]
	if val > 0:
		can.drawString(x, y, "%i" % round(val)) 	
	y -= ySpace
	return y

def fillForm(inputData): 

	values = getTaxValues(inputData)

	packet = StringIO.StringIO()
	ySpace = 12
	x = 500
	x2 = 390
	x3 = 280

	# create a new PDF with Reportlab
	can = canvas.Canvas(packet, pagesize=letter)
	initPage(can)

	# page 1
	# personal info
	info = inputData['info']
	can.drawString(40, 700, info['first_name'])
	can.drawString(225, 700, info['last_name'])
	can.drawString(470, 700, "  ".join(info['ss']))
	can.drawString(40, 650, info['address'])
	city_state_zip = info['city'] + ", " + info['state'] + " " + info['zip']
	can.drawString(40, 625, city_state_zip)
	stat = info['filing_status'] 
	if re.search(r'single', stat):
		can.drawString(133, 591, "x")
	elif re.search(r'sep', stat):
		can.drawString(133, 567, "x")
		can.drawString(233, 555, info['spouse_ss'])
	elif re.search(r'joint', stat):
		can.drawString(133, 579, "x")
	else:
		can.drawString(364, 591, "x")
	can.drawString(139, 543, "x")
	can.drawString(565, 537, "1")
	can.drawString(565, 450, "1")

	# tax numbers
	y = 434
	y = insertValue(can, values, 7, x, y, ySpace)
	y = insertValue(can, values, 8, x, y, ySpace)
	y -= ySpace #can.drawString(x2, y, "%i" % round(values[8])); 	y -= ySpace
	y = insertValue(can, values, 9, x, y, ySpace)
	y = insertValue(can, values, 9, x2, y, ySpace)
	y = insertValue(can, values, 10, x, y, ySpace)
	y = insertValue(can, values, 11, x, y, ySpace)
	y = insertValue(can, values, 12, x, y, ySpace)
	y = insertValue(can, values, 13, x, y, ySpace)
	y = insertValue(can, values, 14, x, y, ySpace)
	#y = insertValue(can, values, 15, x3, y, ySpace)
	y = insertValue(can, values, 15, x, y, ySpace)
	#y = insertValue(can, values, 16, x3, y, ySpace)
	y = insertValue(can, values, 16, x, y, ySpace)
	y = insertValue(can, values, 17, x, y, ySpace)
	y = insertValue(can, values, 18, x, y, ySpace)
	y = insertValue(can, values, 19, x, y, ySpace)
	#y = insertValue(can, values, 20, x3, y, ySpace)
	y = insertValue(can, values, 20, x, y, ySpace)
	y = insertValue(can, values, 21, x, y, ySpace)
	y = insertValue(can, values, 22, x, y, ySpace)
	y = insertValue(can, values, 23, x2, y, ySpace)
	y-= ySpace
	y = insertValue(can, values, 24, x2, y, ySpace)
	y = insertValue(can, values, 25, x2, y, ySpace)
	y = insertValue(can, values, 26, x2, y, ySpace)
	y = insertValue(can, values, 27, x2, y, ySpace)
	y = insertValue(can, values, 28, x2, y, ySpace)
	y = insertValue(can, values, 29, x2, y, ySpace)
	y = insertValue(can, values, 30, x2, y, ySpace)
	y = insertValue(can, values, 31, x2, y, ySpace)
	y = insertValue(can, values, 32, x2, y, ySpace)
	y = insertValue(can, values, 33, x2, y, ySpace)
	y = insertValue(can, values, 34, x2, y, ySpace)
	y = insertValue(can, values, 35, x2, y, ySpace)
	y = insertValue(can, values, 36, x, y, ySpace)
	y = insertValue(can, values, 37, x, y, ySpace)
	can.showPage() # ends page

	# page 2
	initPage(can)
	y = 747
	y = insertValue(can, values, 38, x, y, ySpace)
	y -= ySpace
	y -= ySpace
	y -= ySpace
	y = insertValue(can, values, 40, x, y, ySpace)
	y = insertValue(can, values, 41, x, y, ySpace)
	y = insertValue(can, values, 42, x, y, ySpace)
	y = insertValue(can, values, 43, x, y, ySpace)
	y = insertValue(can, values, 44, x, y, ySpace)
	y = insertValue(can, values, 45, x, y, ySpace)
	y = insertValue(can, values, 46, x, y, ySpace)
	y = insertValue(can, values, 47, x, y, ySpace)
	y = insertValue(can, values, 48, x2, y, ySpace)
	y = insertValue(can, values, 49, x2, y, ySpace)
	y = insertValue(can, values, 50, x2, y, ySpace)
	y = insertValue(can, values, 51, x2, y, ySpace)
	y = insertValue(can, values, 52, x2, y, ySpace)
	y = insertValue(can, values, 53, x2, y, ySpace)
	y = insertValue(can, values, 54, x2, y, ySpace)
	y = insertValue(can, values, 55, x, y, ySpace)
	y = insertValue(can, values, 56, x, y, ySpace)
	y = insertValue(can, values, 57, x, y, ySpace)
	y = insertValue(can, values, 58, x, y, ySpace)
	y = insertValue(can, values, 59, x, y, ySpace)
	y = insertValue(can, values, 60, x, y, ySpace)
	y -= ySpace #y = insertValue(can, values, 60, x, y, ySpace)
	y = insertValue(can, values, 61, x, y, ySpace)
	y = insertValue(can, values, 62, x, y, ySpace)
	y = insertValue(can, values, 63, x, y, ySpace)
	y = insertValue(can, values, 64, x2, y, ySpace)
	y = insertValue(can, values, 65, x2, y, ySpace)
	y = insertValue(can, values, 66, x2, y, ySpace)
	y -= ySpace #y = insertValue(can, values, 66, x3, y, ySpace)
	y = insertValue(can, values, 67, x2, y, ySpace)
	y = insertValue(can, values, 68, x2, y, ySpace)
	y = insertValue(can, values, 69, x2, y, ySpace)
	y = insertValue(can, values, 70, x2, y, ySpace)
	y = insertValue(can, values, 71, x2, y, ySpace)
	y = insertValue(can, values, 72, x2, y, ySpace)
	y = insertValue(can, values, 73, x2, y, ySpace)
	y = insertValue(can, values, 74, x, y, ySpace)
	y = insertValue(can, values, 75, x, y, ySpace)
	y = insertValue(can, values, 76, x, y, ySpace)
	y -= ySpace
	y -= ySpace
	y = insertValue(can, values, 77, x2, y, ySpace)
	y = insertValue(can, values, 78, x, y, ySpace)
	y = insertValue(can, values, 79, x2, y, ySpace)
	can.drawString(194, 230, "   ".join(info['routing_number']))
	can.drawString(194, 218, "   ".join(info['account_number']))
	can.drawString(364, 230, "x")
	can.drawString(329, 110, info['occupation'])
	can.showPage() # ends page

	# eof
	can.save()

	# move to the beginning of the StringIO buffer
	packet.seek(0)
	newPdf = PdfFileReader(packet)
	return newPdf

def generateForm(inputData):

	# create form with values
	newPdf = fillForm(inputData)

	# read your existing PDF
	inputPdf = PdfFileReader(file("f1040.pdf", "rb"))

	# merge input pdf and new pdf together into the output pdf
	outputPdf = PdfFileWriter()
	for i in range(inputPdf.numPages):
		page = inputPdf.getPage(i)
		page.mergePage(newPdf.getPage(i))
		outputPdf.addPage(page)

	# finally, write output pdf file
	outputStream = StringIO.StringIO()
	outputPdf.write(outputStream)
	return outputStream

if __name__ == '__main__':
	main()
