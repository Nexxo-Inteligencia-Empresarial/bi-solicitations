import streamlit as st


def Navbar():
    with st.sidebar:
        st.page_link('app.py', label='Geral')
        st.page_link('pages/departaments.py', label='Departamentos')
        st.page_link('pages/depataments_bar_chart.py', label='Departamentos (Barras)')
        st.page_link('pages/dash_sla.py', label='SLA')
        st.page_link('pages/dash_sla_bar_chart.py', label='Evolução do SLA')
        st.page_link('pages/table_solicitations.py', label='Solicitações Abertas')
