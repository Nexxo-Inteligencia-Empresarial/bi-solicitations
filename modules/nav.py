import streamlit as st


def Navbar():
    with st.sidebar:
        st.page_link('app.py', label='Geral')
        st.page_link('pages/departaments.py', label='Departamentos')
