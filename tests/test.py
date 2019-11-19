import Repeat_API as rep

reference = '/home/michael/data/genomes/SacCer3.fasta'#'simple.fasta'
query = 'A'
lookOnRevComplement = True
minimumRepeatLength = 30 #should be none or positive int

fasta = rep.IO(reference)
info = rep.findRepeats(fasta,query,lookOnRevComplement)
rep.writeBed(query+'.bed',info,minimumRepeatLength)
rep.freqPlot(query+'.pdf',info)
