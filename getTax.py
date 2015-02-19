#!/usr/bin/python
#
# Taken from IRS publication 505: Tax Witholding and Estimated Tax
# Tax Computation Worksheet
#

import string
import re
import sys
import csv


class Data:
	upper = None
	factor = None
	sub = None

# read_p505 function
#
def read_p505(filename):
	data = {}
	upper = []
	factor = []
	sub = []
	key = None
	mode = 'NONE'

	fin = open(filename, 'r')
	for line in fin.readlines():

		if len(line) > 0:
			m = re.search(r'[abcd]?\. [a-zA-Z ()]+\.', line)
			if m:
				n = re.findall(r'\w+', m.group())
				key = n[1].lower()
				if len(n) > 2:
					key = n[1].lower() + '_' + n[2].lower() + '_' + n[3].lower()

			if mode is 'NONE' and line.startswith('$'):
				mode = 'UPPER'

			if mode is 'UPPER':
				try:
					val = line.strip().replace('$','').replace(',','')
					upper.append(float(val))
				except ValueError:
					mode = 'FACTOR' 

			elif mode is 'FACTOR':
				m = re.search(r'[0-9.]+%', line)
				if m:
					val = m.group()[0:-1]
					factor.append(float('.' + val.replace('.', '')))
				else:
					if len(factor) > 0:
						mode = 'SUBTRACT'

			elif mode is 'SUBTRACT':
				try:
					val = line.strip().replace('$','').replace(',','')
					sub.append(float(val))
				except ValueError:
					data[key] = Data()
					data[key].upper = upper
					data[key].factor = factor
					data[key].sub = sub
					upper = []
					factor = []
					sub = []
					mode = 'NONE'

	fin.close()
	return data

# readCsv function
#
def readCsv(filename):
	f = open(filename, 'r')
	reader = csv.reader(f)

	data = {}
	first = True
	header = None
	for row in reader:
		if header is None:
			header = []
			for i in range(len(row)):
				header.append(row[i].strip())
				data[header[i]] = []
		else:
			for i in range(len(row)):
				data[header[i]].append(float(row[i].strip()))

	f.close()
	return data

# calcTax function
#
def calcTax(data, income):
	
	# find tax parameters
	f = None
	s = None
	I = None
	step = 50.0
	if income < 2000:
		step = 25.0
	for i in range(len(data.upper)):
		if income <= data.upper[i]:
			if income <= 99000:
				I = int(income / step) * step + step/2
			else:
				I = income
			f = data.factor[i]
			s = data.sub[i]
			break

	# calculate tax
	tax = I * f - s	
	return tax

# getStatus function
# status can be:
#	single
#	head_of_household
#	married_filing_jointly
#	married_filing_separately
#
def getStatus(arg):
	name = arg.lower()
	if re.search(r'house', name):
		return 'head_of_household'
	if re.search(r'joint', name):
		return 'married_filing_jointly'
	if re.search(r'sep', name):
		return 'married_filing_separately'
	return 'single'

# main function
#
def main():
	if len(sys.argv) >= 2:

		# get arguments
		status = 'single'
		if len(sys.argv) >= 3:
			status = getStatus(sys.argv[2])
		income = float(sys.argv[1])

		# read data
		#data = readCsv('f505.csv')
		data = read_p505('p505.txt')

		# calculate tax
		tax = calcTax(data[status], income)
		print '%d --> %d' % (round(income), round(tax))

	else:	
		print 'usage: %s <income> <opt:status>' % sys.argv[0]

if __name__ == '__main__':
	main()
