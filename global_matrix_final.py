#! /usr/bin/env/python

#this script takes the output of bedtools merge and a text file list of the samples that were merged

#it outputs a matrix with a header
#the first column is a unique identifier: chr_start_stop
#run like this:  python global_matrix_final_11.2.15.py merged_bed_data.merge merged_sample_list.txt

import string
import collections
import glob
import math
import sys

def main():
    #bring in the name of the merged file
    masterName = sys.argv[1] 
    factorList = string.split(masterName, '_')
    
    #generic way to make a name for matrix files.
    factorName = factorList[0] + factorList[1] 
    
    #this identifies the individual files merged into the merge file
    peakFileName = sys.argv[2]   
    peakFiles = open(peakFileName, 'rU')
	
	#remove newlines from the file of peak sample names
    mergePeakFiles = [string.rstrip(line) for line in peakFiles]
    
    #instantiate a sample dict to store the samples in.
    sampleDict = {}

    for colNum,sample in enumerate(mergePeakFiles):
        samp = string.strip(sample) #remove whitespace
        sampleDict[samp] = colNum #notable, colnum is just giving a value to the key
	
	#prints to the console/terminal
    print sampleDict
    
    #open the .merge.final file to process it into a matrix:
    masterPeakFile = open(masterName, 'rU')

    #defining how many columns the file will have based on # samples
    rowLen = len(mergePeakFiles)
	
	#set to blank so we can output by chromosome
    prevChrom = ''
    
    #actually looping through the merge file to make a matrix
    for line in masterPeakFile:
        #merge files are separated by tabs, chrom, start, stop, semicolon delimited samples, semicolon delimited scores
        masterLineList = string.split(line, '\t') #a list for each line.
		#version for chr_start_stop (no gene name included):
        identifier = masterLineList[0] + ':' + masterLineList[1] + '_' + masterLineList[2] 
		
		#define the chromosome we are processing.
        currChrom = masterLineList[0]
        if prevChrom != currChrom:
            #need to re-initialize and make a new image/matrix file
            if prevChrom != '':#if it's not the first time through the file
                #output to a file using outputMatrix
                outputMatrix(rowList, chrLocList, prevChrom, factorName, sampleDict, rowLen)
            #reset these for the next chromosome
            chrLocList = [] #need to store the chrom and loc for each column here    
            rowList = []
            prevChrom = currChrom
        
        #dealing with masterLineList[3](names) and [4](scores)
        scoreList = [float (string.strip(__)) for __ in string.split(masterLineList[4], ',')]
        sampKey = string.split(masterLineList[3], ',')
        #make linked tuples of the two
        sampScore = zip(sampKey, scoreList)

        #fill the row full of zeroes based on the # of samples 
        row = [0.0 for __ in range(rowLen)]
        #obtains the value for a given index in the row
        for key,score in sampScore:
            index = sampleDict.get(key)
            #print "index:", index, "key:", key
            row[index] = score
		
		#add the values and identifier to each row
        rowList.append(row)
        chrLocList.append(identifier)
        
    #at the very end of this, send the last chromosome (likely ChrY) to output matrix as well.
    #prevChrom should be equal to currChrom
    outputMatrix(rowList, chrLocList, prevChrom, factorName, sampleDict, rowLen)

def outputMatrix(rowList, chrLocList, prevChrom, factorName, sampleDict, rowLen):

    #open a file for this chrom to write data to
    matrixFile = open('cluster/' + prevChrom + factorName + '.matrix', 'w')

    #write column headers
    #define the last column, don't tab afterwards
    matrixFile.write('Master_Location_List' + '\t')
    for i,label in enumerate(sorted(sampleDict)):
        if rowLen - i == 1:
            matrixFile.write(label)
        else:
            matrixFile.write(label + '\t')  
    matrixFile.write('\n') 
        
    #writing the actual matrix data to a file:  
    for i,item in enumerate(rowList): #each item in rowList should be a list
        matrixFile.write(chrLocList[i] + '\t')
        for i,elem in enumerate(item):
            if len(item) - i == 1: #should be the last column in a line
                if elem == 0.0:
                    matrixFile.write(' ')#hence the whitespace!! 5/22/16 trying with 0.0!
                else:               
                    matrixFile.write(str(elem))#convert to a string and write to the file
            else:
                if elem == 0.0:
                    matrixFile.write(' ' + '\t') #5/22/16 trying with 0.0!
                else:
                    matrixFile.write(str(elem) + '\t')
                    
        	#newline at the end of each row:
    	matrixFile.write('\n')
    matrixFile.close()
    
main()
