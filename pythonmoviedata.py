import streamlit as st
import pandas as pd
import numpy as np

st.write("Hello Blue Power")
st.write("Get visual based on movie name. contact CKU for info")
x = st.text_input("Movie", "Star Wars")

if st.button("Submit"):
    st.write(f"Your favorite movie is `{x}`")


data = pd.read_csv("movies.csv")
st.write(data)


chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.bar_chart(chart_data)