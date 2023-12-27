import streamlit as st
from helper import getQAchain


st.title("Q/A session")
st.button("Create New Database")
question = st.text_input("Question: ")

if question:
    chain = getQAchain()
    response = chain(question)


    st.header("Answer: ")
    st.write(response['result'])

