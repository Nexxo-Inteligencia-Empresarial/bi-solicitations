import streamlit as st

from src.data.use_cases.interface.get_tickets import GetTickets

class TableSolicitations:

    def __init__(self, use_case:GetTickets, ft_dpt, ft_stts):
        datas = use_case.get_open_tickets(ft_dpt, ft_stts)
        st.dataframe(datas, height=500)
