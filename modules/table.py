import pandas as pd
import streamlit as st

class Table ():

    def __init__(self, sla_exceeded: list[dict]):
        self._renomed_columns = {
            "ticket_id": "ID",
            "departament": "Departamento",
            "system": "Sistema",
            "type": "Tipo",
            "create_date": "Data de Criação",
            "conclusion_date": "Data de Conclusão",
            "days_to_conclusion": "Dias para Conclusão",
        }
        self.__render(sla_exceeded)

    def __render(self, sla_exceeded: list[dict]):
        st.subheader("Solicitações Fora do SLA")
        if sla_exceeded:
            df_fora = pd.DataFrame(sla_exceeded).rename(columns=self._renomed_columns)
            st.dataframe(df_fora)
        else:
            st.info("Nenhuma solicitação fora do SLA encontrado.")