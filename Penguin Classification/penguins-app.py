import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
st.set_page_config(layout="wide")

st.write("""
# Penguin Prediction App

         
This app predicts the **Palmer Penguin** species!
         
""")

st.sidebar.header('User Input Features')

st.sidebar.markdown("""
[Example CSV Input File]
""")

uploaded_file=st.sidebar.file_uploader("Upload Your CSV File", type=['csv'])
if uploaded_file is not None:
    input_df=pd.read_csv(uploaded_file)
else:
    def user_input_features():
        island = st.sidebar.selectbox('Island', ('Biscoe', 'Dream', 'Torgersen'))
        sex=st.sidebar.selectbox('Sex',('male','female'))
        bill_length_mm = st.sidebar.slider('Bill Length (mm)', 32.1,59.6,43.9)
        bill_depth_mm=st.sidebar.slider('Bill Depth (mm)',13.1,21.5,17.2)
        flipper_length_mm = st.sidebar.slider('Flipper Length (mm)', 172.0,231.0,201.0)
        body_mass_g = st.sidebar.slider('Body Mass (g)', 2700.0,6300.0,4207.0)
        data = {
            'island':island,
            'bill_length_mm':bill_length_mm,
            'bill_depth_mm':bill_depth_mm,
            'flipper_length_mm':flipper_length_mm,
            'body_mass_g':body_mass_g,
            'sex':sex

        }
        features=pd.DataFrame(data,index=[0])
        return features
    input_df=user_input_features()


# concatenations of User input and Dataset for encoding
penguins_raw=pd.read_csv('penguins_cleaned.csv')
penguins=penguins_raw.drop(columns=['species'])
df=pd.concat([input_df,penguins],axis=0)

# encoding of ordinal features
encode=['sex','island']
for col in encode:
    dummy=pd.get_dummies(df[col],prefix=col)
    df=pd.concat([df,dummy],axis=1)
    del df[col]
df=df[:1]

#Display the user input Features
st.subheader('User Input Features')

if uploaded_file is not None:
    st.write(df)
else:
    st.write('Awaiting CSV File to be Uploaded. Currently Using example input parameters')
    st.write(df)

#read saved Classification model

load_clf=pickle.load(open('penguins_clf.pkl','rb'))


#Apply the model to make prediction
prediction=load_clf.predict(df)
prediction_proba=load_clf.predict_proba(df)

st.subheader('Prediction')
penguins_species=np.array(['Adelie','Chinstrap','Gentoo'])

st.write(penguins_species[prediction])
st.subheader("Prediction Probability")
st.write(prediction_proba)