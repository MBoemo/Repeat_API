import Repeat_API as rep

reference = '/home/michael/data/genomes/SacCer3.fasta'#'simple.fasta'#
query = 'CGG'
lookOnRevComplement = True
minimumRepeatLength = None #should be none or positive int

bed = rep.parseRepeats(reference,query,lookOnRevComplement,minimumRepeatLength)
