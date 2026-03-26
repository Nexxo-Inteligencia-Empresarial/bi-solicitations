import streamlit as st

class TableSlaExceded():

    def __init__(self, datas):
        self.__render(datas)

    def __render(self, sla_exceded: list[dict]):
        st.subheader("Solicitações Fora do SLA")
        if sla_exceded:
            st.dataframe(sla_exceded, height=500)
        else:
            st.info("Nenhuma solicitação fora do SLA encontrado.")
