import streamlit as st
import os
import pandas as pd
import glob

st.title('API behaviour input')

file_path = os.path.join(os.getcwd(),'data','input.txt') 
data = []
with open(file_path, "r") as file_object:
    # Move read cursor to the start of file.
    file_object.seek(0)
    # If file is not empty then append '\n'
    for r in file_object.readlines():
        data.append(r)

st.write(F"Current stack has {len(data)} inputs")



with st.beta_expander('Show inputs'):

    s = pd.DataFrame({'SNo':[x+1 for x in range(len(data))],
                      'Input':data})
    st.markdown(s.to_markdown())