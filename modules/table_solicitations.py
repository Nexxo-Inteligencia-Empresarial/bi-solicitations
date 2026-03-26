import streamlit as st

class TableSolicitations():

    def __init__(self, datas):
        st.dataframe(datas, height=500)
