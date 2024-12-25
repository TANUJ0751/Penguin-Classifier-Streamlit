import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image


image=Image.open('dna-logo.jpg')

st.write("""
# DNA Nucleotide Count Web App
 This app counts necleotide composition of query DNA!
***
""")
st.image(image,use_column_width=True)


#input text box

st.header("Enter DNA Sequence")
sequence_input = ">DNA Query\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"


sequence=st.text_area("Sequence Input",sequence_input,height=200)
sequence=''.join(sequence.splitlines()[1:])


st.write("""
***
""")

#prints the input Dna Sequence
st.header('INPUT (DNA Query)')
sequence


#DNA Nucleotide Count
st.header('OUTPUT (DNA Nucleotide Count)')

# Print Dictionary

st.subheader('1. Print Dictionary')
def DNA_nucleotide_count(seq):
    d=dict([('A',seq.count('A')),
            ('T',seq.count('T')),
            ('G',seq.count('G')),
            ('C',seq.count('C'))
            ])
    return d

X=DNA_nucleotide_count(sequence)
X_label=list(X)
X_values=list(X.values())

X

#Print Text

st.subheader('2. Print Text')

st.write('There Are '+str(X['A'])+' adenine(A)')
st.write('There are '+str(X['T'])+'thymine(T)')
st.write('There are '+str(X['G'])+' guanine(G)')
st.write('There are '+str(X['C'])+' cytosine(C)')

# Disply the DataFrame
st.subheader('3. Display DataFrame')
df=pd.DataFrame.from_dict(X,orient='index')
df=df.rename({0:'Count'},axis='columns')
df.reset_index(inplace=True)
df=df.rename(columns={'index':'Nucleotide'})
st.write(df)


# Display Bar Chart Using Altair
st.subheader('4. Display Bar Chart')
p=alt.Chart(df).mark_bar().encode(
    x='Nucleotide',
    y='Count'
)
p=p.properties(width=alt.Step(80))

st.write(p)


