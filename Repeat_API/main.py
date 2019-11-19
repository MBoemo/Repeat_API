#!/usr/bin/env python

#----------------------------------------------------------
# Written by Michael A. Boemo (mb915@cam.ac.uk)
# This software is licensed under MIT.  You should have
# received a copy of the license with this software.  If
# not, please Email the author.
#----------------------------------------------------------

import warnings
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


def IO(filename):

	fasta_sequences = SeqIO.parse(open(filename),'fasta')
	name2seq = {}
	for contig in fasta_sequences:
		name2seq[contig.id] = (str(contig.seq)).upper()
	return ParsedFasta(filename,name2seq)


def findRepeats(pfasta,repeat):
	
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
				bedTuples.append((contigName,start,end))
				start = idx_next	
			idx = idx_next
	return BedInfo(pfasta.genome,repeat,bedTuples)


def writeBed(outFilename,bed):
	f = open(outFilename,'w')
	f.write('#bed file generated by Repeat_API\n')
	f.write('#contact Michael Boemo (mb915@cam.ac.uk) with any issues\n')
	f.write('#reference genome: '+bed.genome+'\n')
	f.write('#repeat motif: '+ bed.repeat+'\n')
	f.write('#contig\tstart\tend\trepeat length\n')
	for t in bed.bedLines:
		f.write(str(t[0]) + '\t' + str(t[1]) + '\t' + str(t[2]) + '\t' + str(t[2]-t[1])+'\n')
	f.close()


def freqPlot(outFilename,bed):
	lengths = []
	for t in bed.bedLines:
		lengths.append(t[2]-t[1])
	plt.figure()
	plt.hist(lengths,25,log=True)
	plt.xlabel('Repeat Length')
	plt.ylabel('Count')
	plt.title('Distribution of '+bed.repeat+' Repeats')
	plt.savefig(outFilename)
	