from datetime import datetime, date

import streamlit as st
import pandas as pd
import altair as alt

from src.data.use_cases.get_tickets import GetTickets
from src.data.use_cases.get_last_executation import GetLastExecution
from src.infra.db.repositories.tickets_requests_repository import TicketsRequestsRepository
from src.infra.db.repositories.execution_collection_repository import ExecutionCollectionRepository
from modules import Navbar, Header, AutoRefresh, Footer, StatusChart, AlertOutdate


use_case_tickets = GetTickets(TicketsRequestsRepository())
use_case_execution = GetLastExecution(ExecutionCollectionRepository())

st.set_page_config(layout="wide", page_title="BI Solicitations", page_icon="🧊")
st.logo(image='images/logo.png')


def main():
    AutoRefresh()
    Navbar()
    Header()

    datas = use_case_tickets.get_by_departament()
    datas_execution = use_case_execution.get()

    AlertOutdate(datas_execution)

    total_solicitations = sum(sum(status_qtd.values()) for status_qtd in datas.values())

    st.markdown("<h1 style='text-align: center; margin-bottom: 10px'>Solicitações Abertas Acessórias/Onvio</h1>", unsafe_allow_html=True)

    st.markdown(
        f"<h3 style='text-align: center; color: #444; font-weight: normal;'>Total de solicitações: <strong>{total_solicitations}</strong></h3>",
        unsafe_allow_html=True
    )

    datas_itens = list(datas.items())
    datas_itens.sort(key=lambda item: sum(item[1].values()), reverse=True)

    StatusChart(datas_itens)

    for system, last_execution in datas_execution:
        st.markdown(f"""
            <div style="text-align: center; font-size: 16px;">
                <strong>{system.capitalize()}</strong>: {last_execution.strftime('%d/%m/%Y %H:%M:%S')}
            </div>
        """, unsafe_allow_html=True)

    Footer()

if __name__ == '__main__':
    main()
