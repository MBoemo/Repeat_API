#!/usr/bin/env python

#----------------------------------------------------------
# Written by Michael A. Boemo (mb915@cam.ac.uk)
# This software is licensed under MIT.  You should have
# received a copy of the license with this software.  If
# not, please Email the author.
#----------------------------------------------------------

import warnings
import StringIO
import sys
import re
import copy
from Bio import SeqIO
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt


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


def writeBedHeader(f,genome,repeat,minLength):

	f.write('#bed file generated by Repeat_API\n')
	f.write('#contact Michael Boemo (mb915@cam.ac.uk) with any issues\n')
	f.write('#reference genome: '+ genome + '\n')
	f.write('#repeat motif: '+ repeat + '\n')
	f.write('#minimum repeat length: '+ str(minLength)+'\n')
	f.write('#contig\tstart\tend\trepeat length\tstrand\n')


def appendBed(f,bedTuples,minLength):

	for t in bedTuples:

		if minLength is not None:
			if t[2]-t[1] >= minLength:
				f.write(str(t[0]) + '\t' + str(t[1]) + '\t' + str(t[2]) + '\t' + str(t[2]-t[1])+'\t'+t[3]+'\n')
		else:
			f.write(str(t[0]) + '\t' + str(t[1]) + '\t' + str(t[2]) + '\t' + str(t[2]-t[1])+'\t'+t[3]+'\n')


def parseRepeats(filename,repeat,useRC,minLength):

	f = open(repeat+'.bed','w')
	writeBedHeader(f,filename,repeat,minLength)
	lengths = []

	fasta_sequences = SeqIO.index(filename,'fasta')
	for contig in fasta_sequences:

		bedTuples = findRepeats(contig,str(fasta_sequences[contig].seq).upper(),repeat,useRC)
		for t in bedTuples:
			lengths.append(t[2]-t[1])
		appendBed(f,bedTuples,minLength)
	f.close()
	freqPlot(repeat+'.pdf',repeat,lengths)


def findRepeats(contig,seq,repeat,useRC):

	repeat = copy.deepcopy(repeat).upper()
	bedTuples = []

	for match in re.finditer('('+repeat+')+',seq):
		bedTuples.append((contig,match.start(0),match.end(0),'template'))

	if useRC and repeat != reverseComplement(repeat):
		bedTuplesRC = []
		rcRepeat = reverseComplement(repeat)
		for match in re.finditer('('+rcRepeat+')+',seq):
			bedTuplesRC.append((contig,match.start(0),match.end(0),'complement'))
		bedTuples += bedTuplesRC

	return bedTuples


def freqPlot(outFilename,repeat,lengths):
	
	plt.figure()
	plt.hist(lengths,25,log=True)
	plt.xlabel('Repeat Length')
	plt.ylabel('Count')
	plt.title('Distribution of '+repeat+' Repeat Lengths')
	plt.savefig(outFilename)
	
