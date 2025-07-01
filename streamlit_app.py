import streamlit as st
import json 

st.title("Classroom Finder")
st.write(
    "QST"
)

with open("QST.json") as file:
        data = json.load(file)
        st.write(data)
