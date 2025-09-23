import streamlit as st
import pandas as pd

from src.utils.mappings import Mappings
from src.data.use_cases.interface.get_tickets import GetTickets


class SlaCardTable:

    def __init__(self, use_case: GetTickets, ft_dpt, start_date, close_date):
        datas = use_case.sla_per_month(ft_dpt, start_date, close_date)
        self.__render(datas)

    def __render(self, datas):
        meses = sorted(datas.keys())

        tabela = []
        for m in meses:
            dentro = datas[m]["Dentro do SLA"]
            fora = datas[m]["Fora do SLA"]
            tabela.append({
                "Mês": Mappings.months(m),
                "Dentro do SLA": dentro,
                "Fora do SLA": fora
            })

        df = pd.DataFrame(tabela)

        with st.container():
            st.subheader("Resumo mensal")

            with st.expander("📋 Ver tabela completa"):
                st.dataframe(
                    df,
                    hide_index=True,
                    use_container_width=True
                )
