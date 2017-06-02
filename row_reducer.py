#! /usr/bin/env/python
#row_reducer.py

#2017_01_25: added this back in: line = string.rstrip(line, '\n')  because newlines are counted as "non blank" and this throws the numbers off
#also added that numrow should be reported as numRow-1 at the end, to avoid the confound of the header in the count

#usage: python row_reducer.py file.matrix n
#file.matrix is the product of global_matrix.py (or any of it's derivatives)
#n is the number of items per row that should be non-whitespace
#the output is in the matrix format, but constrained to rows
#that meet the column selection criteria

import math
import sys
import string

def main():
	
	#read in the file
	matrixFileName = sys.argv[1]
	#number of columns to require non-blank value
	numCol = int(sys.argv[2])
	matrixFile = open(matrixFileName, 'rU')
	newMatrixFile = open(matrixFileName + '.txt', 'w')
	numRow = 0
	
	for line in matrixFile:
		line = string.rstrip(line, '\n') #strip off ONLY newlines
		row = string.split(line, '\t')#should split into entries
		rowNotNullCount = 0
		
		for entry in row[1:]:
			if entry != ' ': 
				rowNotNullCount = rowNotNullCount + 1
			else: #the item is whitespace
				rowNotNullCount = rowNotNullCount + 0 
	
		if rowNotNullCount >= numCol:
			newMatrixFile.write(line)
			newMatrixFile.write('\n') #or everything is on a single line!!
			numRow = numRow + 1
		else:
			continue
	#when the newMatrixfile writing is done
	newMatrixFile.close()
	print "Total Number rows in output file: ", numRow-1 #note that this doesn't include the header

main()
