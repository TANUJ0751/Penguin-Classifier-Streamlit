import numpy as np
import pandas as pd
import streamlit as st
import pickle
from PIL import Image
from rdkit import Chem
from rdkit.Chem import Descriptors


def AromaticProportion(m):
    aromatic_atoms=[m.GetAtomWithIdx(i).GetIsAromatic() for i in range(m.GetNumAtoms())]
    aa_count=[]
    for i in aromatic_atoms:
        if i==True:
            aa_count.append(1)
    AromaticAtom=sum(aa_count)
    HeavyAtom=Descriptors.HeavyAtomCount(m)
    AR=AromaticAtom/HeavyAtom
    return AR

def generate(smiles,verbose=False):
    moldata= []
    for elem in smiles:
        mol=Chem.MolFromSmiles(elem)
        moldata.append(mol)

    baseData= np.arange(1,1)
    i=0
    for mol in moldata:

        desc_MolLogP = Descriptors.MolLogP(mol)
        desc_MolWt = Descriptors.MolWt(mol)
        desc_NumRotatableBonds = Descriptors.NumRotatableBonds(mol)
        desc_AromaticProportion = AromaticProportion(mol)

        row = np.array([desc_MolLogP,
                        desc_MolWt,
                        desc_NumRotatableBonds,
                        desc_AromaticProportion])

        if(i==0):
            baseData=row
        else:
            baseData=np.vstack([baseData, row])
        i=i+1

    columnNames=["MolLogP","MolWt","NumRotatableBonds","AromaticProportion"]
    descriptors = pd.DataFrame(data=baseData,columns=columnNames)

    return descriptors

#Title
image=Image.open('solubility-logo.jpg')
st.image(image, use_column_width=True)
st.write(""" # Molecular Solubility Prediction App
This app Predicts the **Solubility (LogS)** values of Molecules!
Data Obtained from the John S. Delaney.[ESOL: Estimation Aqueous Solubility Directly from Molecular Structure]
          """)
st.sidebar.header("User Input Features")
SMILES_input="NCCCC\nCCC\nCN"
SMILES=st.sidebar.text_area("SMILES input",SMILES_input)
SMILES="C\n"+SMILES # adds C as Dummy, first item
SMILES=SMILES.split('\n')

st.header('Input SMILES')
SMILES[1:] #Skips dummy first Item

#Calculate Molecular Descriptors
st.header('Computed Molecular Description')

X=generate(SMILES)
X[1:] #Skips the Dummy first Item


#load model

load_model=pickle.load(open('solubility_model.pkl','rb'))

prediction=load_model.predict(X)
#prediction_proba=load_model.predict_proba(X)

st.header('Predicted LogS Values')
prediction[1:]
#prediction
