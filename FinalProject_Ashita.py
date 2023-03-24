
# coding: utf-8

# In[1]:


from Bio import SeqIO
import pandas as pd
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from Bio.Seq import Seq
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML


# In[2]:


#importing and reading the file to use 
for seq_record in SeqIO.parse("Aeromonas veroni.fna", "fasta"):
    print("record id is",seq_record.id)
    dna_sense= seq_record.seq
    print("Length of DNA SEquence is",len(seq_record))


# In[3]:


def complement(dna):
    """
    compute the complement of the fasta dna sequence 

    Arguments:
        dna: string
    """
    basecomplement = {'A':'T', 'C':'G','G':'C', 'T':'A', 'N':'N'}
    letters = list(dna)
    letters = [basecomplement[base] for base in letters]
    return ''.join(letters) 


# In[4]:


dna_antisense=complement(dna_sense)


# In[5]:


def startstop_codon(dna, frame):
    """
    compute the start stop codon to find the ORF's 

    Arguments:
        dna: string
        frame: integer from 0 to 2 
    """
    #dna = dna.upper()
    for i in range(frame, len(dna), 3):
        codon1 = dna[i:i+3]
        if codon1 == 'ATG':
            position1 = i
            for j in range(position1, len(dna), 3):
                codon2 = dna[j:j+3]
                if codon2 in ['TAA', 'TAG', 'TGA']:
                    position2 = j
                    yield (position2-position1+3, dna[position1:position2+3])
                    break


# In[6]:


def potential_orf(dna):
    """
    compute the potential ORF for the  given dna sequence in fasta format

    Arguments:
        dna: string
    """
    Potential_orf_list = []
    potential_orf_length=[]
    for orflen, orf in startstop_codon(dna , 0):
        if orflen >50: #check if the length is greater than 50 and only return those results
            Potential_orf_list.append(str(orf))
            potential_orf_length.append(orflen)
    return Potential_orf_list,potential_orf_length
        


# In[7]:


potential_orf_sense, potential_length_sense = potential_orf(dna_sense)
potential_orf_antisense, potential_length_antisense = potential_orf(dna_antisense)


# In[8]:


# for orflen, orf in startstop_codon(dna_strand2 , 0):
#     if orflen >50:
#         print(orflen, orf)


# In[9]:


# Python program to convert
# altered DNA to protein
def translate(seq):
    """
    compute the translate for the  given dna sequence to protein

    Arguments:
        seq: string
    """
      
    table = {
        'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
        'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',                 
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
        'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
        'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
        'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
        'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
        'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
    }
    protein =""
    if len(seq)%3 == 0:
        for i in range(0, len(seq), 3):
            codon = seq[i:i + 3]
            protein+= table[codon]
    return protein
def read_seq(Orf_list):
    Protein_Orf = []
    for orf in Orf_list:
        Protein_Orf.append(translate(orf))
    return Protein_Orf


# In[10]:


#Protein_sense translated to the protein
protein_sense = read_seq(potential_orf_sense)
protein_sense


# In[11]:


#  #5 Protein_sense translated to the protein results converting to Seq
# BlastSequence = [protein for protein in protein_sense if len(protein)<1000]
# BlastSequence = [Seq((protein) for protein in protein_sense]
# BlastSequence


# In[12]:


#To get the first 5 
BlastSequence = []
for protein in protein_sense:
    if len(protein)<1000:
        BlastSequence.append(protein)
    if len(BlastSequence)== 5:
        break
BlastSequence


# In[13]:


#Protein_antisense translated to the protein
protein_antisense = read_seq(potential_orf_antisense)
protein_antisense


# In[14]:


def mol_wt(protein_list):
    """
    compute the molecular weight for the  given protein

    Arguments:
        protein_list: string
    """
    protein_mol_wt = []
    for protein in protein_list:
        weights = {'A': 89, 'C': 121, 'D': 133, 'E': 147, 'F': 165,
       'G': 75, 'H': 155, 'I': 131, 'K': 146, 'L': 131,
       'M': 149, 'N': 132, 'P': 115, 'Q': 146, 'R': 174,
       'S': 105, 'T': 119, 'V': 117, 'W': 204, 'Y': 181, '_' : 0 }
        weight = sum(weights[p] for p in protein) / 1000
        protein_mol_wt.append("%0.2f" % weight)
    return protein_mol_wt


# In[15]:


#Protein_sense protein Molecular Weight in KDa
proteinsense_molwt = mol_wt(protein_sense)
proteinsense_molwt


# In[16]:


#Protein_antisense protein Molecular Weight in KDa
proteinantisense_molwt = mol_wt(protein_antisense)
proteinantisense_molwt


# In[17]:


def mol_wt_biopython(proteinList):
    """
    compute the molecular weight for the  given protein using biopython module

    Arguments:
        proteinList: string
    """
    
    mol_wt_list = []
    
    for ele in proteinList:
            y = ele[0:len(ele)-1]
            X = ProteinAnalysis(y)
            C = X.molecular_weight()/1000
            mol_wt_list.append("%0.2f" % C)
    return mol_wt_list 


# In[18]:


#Protein_sense protein Molecular Weight in KDa
proteinsense_molwtbiopython = mol_wt_biopython(protein_sense)
proteinsense_molwtbiopython


# In[19]:


#Protein_antisense protein Molecular Weight in KDa
proteinantisense_molwtbiopython = mol_wt_biopython(protein_antisense)
proteinantisense_molwtbiopython


# In[20]:


#Making the data look neatly using DataFrame for sense strand
sense_df = pd.DataFrame({'potential_length_sense' : potential_length_sense,'potential_orf_sense' : potential_orf_sense ,'protein_sense':protein_sense,'proteinsense_molwt' : proteinsense_molwt,'proteinsense_molwtbiopython' : proteinsense_molwtbiopython }, columns=['potential_length_sense','potential_orf_sense', 'protein_sense','proteinsense_molwt','proteinsense_molwtbiopython']) 


# In[21]:


sense_df


# In[22]:


sense_df .to_csv("sense.csv") #Converting the DataFrame to csv


# In[41]:


#Making the data look neatly using DataFrame for antisense strand
antisense_df = pd.DataFrame({'potential_length_antisense' : potential_length_antisense,'potential_orf_antisense' : potential_orf_antisense ,'protein_antisense':protein_antisense,'proteinantisense_molwt' : proteinantisense_molwt ,'proteinantisense_molwtbiopython': proteinantisense_molwtbiopython}, columns=['potential_length_antisense','potential_orf_antisense', 'protein_antisense','proteinantisense_molwt','proteinantisense_molwtbiopython'])


# In[42]:


antisense_df


# In[43]:


antisense_df .to_csv("antisense.csv") #Converting the DataFrame to csv


# In[26]:


result_handle1 = NCBIWWW.qblast("blastp", "nr", BlastSequence[0])


# In[27]:


with open('Blast_seq1.xml','w') as save_file:
    blastresult1 = result_handle1.read()
    save_file.write(blastresult1)


# In[28]:


result_handle2 = NCBIWWW.qblast("blastp", "nr", BlastSequence[1])


# In[29]:


with open('Blast_seq2.xml','w') as save_file:
    blastresult2 = result_handle2.read()
    save_file.write(blastresult2)


# In[30]:


result_handle3 = NCBIWWW.qblast("blastp", "nr", BlastSequence[2])


# In[31]:


with open('Blast_seq3.xml','w') as save_file:
    blastresult3 = result_handle3.read()
    save_file.write(blastresult3)


# In[32]:


result_handle4 = NCBIWWW.qblast("blastp", "nr", BlastSequence[3])


# In[33]:


with open('Blast_seq4.xml','w') as save_file:
    blastresult4 = result_handle4.read()
    save_file.write(blastresult4)


# In[34]:


result_handle5 = NCBIWWW.qblast("blastp", "nr", BlastSequence[4])


# In[35]:


with open('Blast_seq5.xml','w') as save_file:
    blastresult5 = result_handle5.read()
    save_file.write(blastresult5)


# In[36]:


E_VALUE_THRESH = 1e-20
for record in NCBIXML.parse(open("Blast_seq1.xml")):
        if record.alignments:
            print("\n")
            print("query Sequence1: %s" % BlastSequence[0])
            for align in record.alignments:
                for hsp in align.hsps:
                    if hsp.expect < E_VALUE_THRESH:
                        print('****Alignment****')
                        print('sequence:', alignment.title)
                        print('length:', alignment.length)
                        print('e value:', hsp.expect)
                        print('score:', hsp.score)
                        print(hsp.query)
                        print(hsp.match)
                        print("**")


# In[37]:


E_VALUE_THRESH = 1e-20
for record in NCBIXML.parse(open("Blast_seq2.xml")):
        if record.alignments:
            print("\n")
            print("query Sequence2: %s" % BlastSequence[1])
            for align in record.alignments:
                for hsp in align.hsps:
                    if hsp.expect < E_VALUE_THRESH:
                        print('****Alignment****')
                        print('sequence:', alignment.title)
                        print('length:', alignment.length)
                        print('e value:', hsp.expect)
                        print('score:', hsp.score)
                        print(hsp.query)
                        print(hsp.match)
                        print("**")


# In[38]:


E_VALUE_THRESH = 1e-20
for record in NCBIXML.parse(open("Blast_seq3.xml")):
        if record.alignments:
            print("\n")
            print("query Sequence3: %s" % BlastSequence[2])
            for align in record.alignments:
                for hsp in align.hsps:
                    if hsp.expect < E_VALUE_THRESH:
                        print('****Alignment****')
                        print('sequence:', alignment.title)
                        print('length:', alignment.length)
                        print('e value:', hsp.expect)
                        print('score:', hsp.score)
                        print(hsp.query)
                        print(hsp.match)
                        print("**")


# In[39]:


E_VALUE_THRESH = 1e-20
for record in NCBIXML.parse(open("Blast_seq4.xml")):
        if record.alignments:
            print("\n")
            print("query Sequence4: %s" % BlastSequence[3])
            for align in record.alignments:
                for hsp in align.hsps:
                    if hsp.expect < E_VALUE_THRESH:
                        print('****Alignment****')
                        print('sequence:', alignment.title)
                        print('length:', alignment.length)
                        print('e value:', hsp.expect)
                        print('score:', hsp.score)
                        print(hsp.query)
                        print(hsp.match)
                        print("**")


# In[40]:


E_VALUE_THRESH = 1e-20
for record in NCBIXML.parse(open("Blast_seq5.xml")):
        if record.alignments:
            print("\n")
            print("query Sequence5: %s" % BlastSequence[4])
            for align in record.alignments:
                for hsp in align.hsps:
                    if hsp.expect < E_VALUE_THRESH:
                        print('****Alignment****')
                        print('sequence:', alignment.title)
                        print('length:', alignment.length)
                        print('e value:', hsp.expect)
                        print('score:', hsp.score)
                        print(hsp.query)
                        print(hsp.match)
                        print("**")

