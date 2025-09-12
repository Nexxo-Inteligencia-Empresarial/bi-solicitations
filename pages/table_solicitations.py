

import streamlit as st

from src.data.use_cases.get_tickets import GetTickets
from src.data.use_cases.get_last_executation import GetLastExecution
from src.infra.db.repositories.tickets_requests_repository import TicketsRequestsRepository
from src.infra.db.repositories.execution_collection_repository import ExecutionCollectionRepository
from modules import Navbar, AutoRefresh, Footer
from src.utils.map_categories import categories



use_case_tickets = GetTickets(TicketsRequestsRepository())
use_case_execution = GetLastExecution(ExecutionCollectionRepository())

st.set_page_config(layout="wide", page_title="BI Solicitations", page_icon="🧊")


def main():
    AutoRefresh()

    col1, col2 = st.columns([1,1])
    with col1:
        departaments = st.multiselect(
            "Filtro por departamentos", categories.keys(),
            placeholder="Selecione um departamento"
        )

    with col2:
        status = st.multiselect(
            "Filtro por status", ["Responder", "Resolvendo", "Atrasada"],
            placeholder="Selecione um departamento"
        )


    Navbar()
    if departaments or status:
        datas = use_case_tickets.get_full(departaments, status)
    else:
        datas = use_case_tickets.get_full()
    datas_execution = use_case_execution.get()

    st.dataframe(datas)


    for system, last_execution in datas_execution:
        st.markdown(f"""
            <div style="text-align: center; font-size: 16px;">
                <strong>{system.capitalize()}</strong>: {last_execution.strftime('%d/%m/%Y %H:%M:%S')}
            </div>
        """, unsafe_allow_html=True)

    Footer()

if __name__ == '__main__':
    main()
