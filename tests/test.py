import Repeat_API as rep

reference = 'simple.fasta'
query = 'GC'

fasta = rep.IO(reference)
info = rep.findRepeats(fasta,query)
rep.writeBed(query+'.bed',info)
rep.freqPlot(query+'.pdf',info)
