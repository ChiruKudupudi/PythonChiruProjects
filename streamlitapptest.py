#code
"""
import streamlit as st
import pandas as pd
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

df = load_data("https://github.com/plotly/datasets/raw/master/uber-rides-data1.csv")
st.dataframe(df)

st.button("Rerun")
"""
# Set web page format
import streamlit as st
st.set_page_config(layout="wide")
# Diasble virtual VRAM on windows system
import torch
torch.cuda.set_per_process_memory_fraction(0.999, 0)


st.markdown("""
# DiffSynth Studio

[Source Code](https://github.com/Artiprocher/DiffSynth-Studio)

Welcome to DiffSynth Studio.
""")
