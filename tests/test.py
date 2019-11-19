import Repeat_API as rep

reference = 'simple.fasta'#'/home/michael/data/genomes/SacCer3.fasta'
query = 'GGC'
lookOnRevComplement = True
minimumRepeatLength = None #should be none or positive int

fasta = rep.IO(reference)
info = rep.findRepeats(fasta,query,lookOnRevComplement)
rep.writeBed(query+'.bed',info,minimumRepeatLength)
rep.freqPlot(query+'.pdf',info)
