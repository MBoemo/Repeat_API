#!/usr/bin/env python

#----------------------------------------------------------
# Written by Michael A. Boemo (mb915@cam.ac.uk)
# This software is licensed under MIT.  You should have
# received a copy of the license with this software.  If
# not, please Email the author.
#----------------------------------------------------------

import warnings
import sys
import math
import numpy as np
from Bio import SeqIO
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt


class BedInfo():
	def __init__(self,refFilename,motif,bedTuples):
		self.genome = refFilename
		self.repeat = motif
		self.bedLines = bedTuples


class ParsedFasta():
	def __init__(self,refFilename,name2seq):
		self.genome = refFilename
		self.parsedFasta = name2seq

def reverseComplement(seq):
	newSeq = ''
	for s in seq:
		if s == 'A':
			newSeq += 'T'
		elif s == 'T':
			newSeq += 'A'
		elif s == 'C':
			newSeq += 'G'
		elif s == 'G':
			newSeq += 'C'
		else:
			warnings.warn("Nucleotides must be A, T, G, or C.")
			sys.exit()
			
	return newSeq[::-1]


def IO(filename):

	fasta_sequences = SeqIO.parse(open(filename),'fasta')
	name2seq = {}
	for contig in fasta_sequences:
		name2seq[contig.id] = (str(contig.seq)).upper()
	return ParsedFasta(filename,name2seq)


def findRepeats(pfasta,repeat,useRC):
	
	repeat = repeat.upper()
	bedTuples = []	
	for contigName in pfasta.parsedFasta:
		seq = pfasta.parsedFasta[contigName]
		pos = 0
		idx = seq.find(repeat,0)
		start = idx
		while idx != -1:
			idx_next = seq.find(repeat,idx+len(repeat))
			if idx_next - idx != len(repeat):
				end = idx+len(repeat)
				bedTuples.append((contigName,start,end,'template'))
				start = idx_next	
			idx = idx_next

	if useRC:
		bedTupesRC = []
		for contigName in pfasta.parsedFasta:
			seq = pfasta.parsedFasta[contigName]
			pos = 0
			repeat = reverseComplement(repeat)
			idx = seq.find(repeat,0)
			start = idx
			while idx != -1:
				idx_next = seq.find(repeat,idx+len(repeat))
				if idx_next - idx != len(repeat):
					end = idx+len(repeat)
					bedTupesRC.append((contigName,start,end,'complement'))
					start = idx_next	
				idx = idx_next
		bedTuples += bedTupesRC

	return BedInfo(pfasta.genome,repeat,bedTuples)


def writeBed(outFilename,bed,minLength):
	f = open(outFilename,'w')
	f.write('#bed file generated by Repeat_API\n')
	f.write('#contact Michael Boemo (mb915@cam.ac.uk) with any issues\n')
	f.write('#reference genome: '+bed.genome+'\n')
	f.write('#repeat motif: '+ bed.repeat+'\n')
	f.write('#minimum repeat length: '+ str(minLength)+'\n')
	f.write('#contig\tstart\tend\trepeat length\tstrand\n')
	for t in bed.bedLines:

		if minLength is not None:
			if t[2]-t[1] >= minLength:
				f.write(str(t[0]) + '\t' + str(t[1]) + '\t' + str(t[2]) + '\t' + str(t[2]-t[1])+'\t'+t[3]+'\n')
		else:
			f.write(str(t[0]) + '\t' + str(t[1]) + '\t' + str(t[2]) + '\t' + str(t[2]-t[1])+'\t'+t[3]+'\n')
	f.close()


def freqPlot(outFilename,bed):
	lengths = []
	for t in bed.bedLines:
		lengths.append(t[2]-t[1])
	plt.figure()
	plt.hist(lengths,25,log=True)
	plt.xlabel('Repeat Length')
	plt.ylabel('Count')
	plt.title('Distribution of '+bed.repeat+' Repeat Lengths')
	plt.savefig(outFilename)
	
