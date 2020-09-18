import numpy as np
import collections
from nltk.corpus import stopwords

data = """
A section of DNA that contains instructions to make a protein is called a gene. Each gene has the sequence for at least one polypeptide. Proteins form structures, and also form enzymes. The enzymes do most of the work in cells. Proteins are made out of smaller polypeptides, which are formed of amino acids. To make a protein to do a particular job, the correct amino acids have to be joined up in the correct order. Proteins are made by tiny machines in the cell called ribosomes. Ribosomes are in the main body of the cell, but DNA is only in the nucleus of the cell. The codon is part of the DNA, but DNA never leaves the nucleus. Because DNA cannot leave the nucleus, the cell makes a copy of the DNA sequence in RNA. This is smaller and can get through the holes  pores  in the membrane of the nucleus and out into the cell. Genes encoded in DNA are transcribed into messenger RNA (mRNA) by proteins such as RNA polymerase. Mature mRNA is then used as a template for protein synthesis by the ribosome. Ribosomes read codons, 'words' made of three base pairs that tell the ribosome which amino acid to add. The ribosome scans along an mRNA, reading the code while it makes protein. Another RNA called tRNA helps match the right amino acid to each codon.
"""

STOP = set(stopwords.words('english'))

def main():
	data = read_file()
	data_no_stop = ' '.join([x for x in data[0].split(' ') if x.lower() not in STOP])

	word_freq = list(dict(collections.Counter(data_no_stop.split())).items())
	word_freq.sort(key = lambda x: -x[1])

	sentences = data[0].split('.')[:-1]
	top_4_sentence_indices = list({i: sum([j.count(k) for k in np.array(word_freq)[:4,0]]) for i,j in enumerate(sentences)}.items())
	top_4_sentence_indices.sort(key = lambda x: -x[1])
	top_four = list(np.array(top_4_sentence_indices)[:4,0])
	top_four.sort()

	print('. '.join([sentences[i] for i in top_four])+'.')

if __name__ == '__main__':
	main()
