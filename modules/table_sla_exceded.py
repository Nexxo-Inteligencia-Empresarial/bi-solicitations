import streamlit as st

from src.data.use_cases.interface.get_tickets import GetTickets
class TableSlaExceded():

    def __init__(self, use_case: GetTickets, ft_dpt, start_date, end_date):
        datas = use_case.get_sla_exceded(ft_dpt, start_date, end_date)
        self.__render(datas)

    def __render(self, sla_exceded: list[dict]):
        st.subheader("Solicitações Fora do SLA")
        if sla_exceded:
            st.dataframe(sla_exceded, height=500)
        else:
            st.info("Nenhuma solicitação fora do SLA encontrado.")
