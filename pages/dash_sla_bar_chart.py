import streamlit as st
import plotly.graph_objects as go
from uuid import uuid4
from src.data.use_cases.get_tickets import GetTickets
from src.infra.db.repositories.tickets_requests_repository import TicketsRequestsRepository
from src.utils.map_categories import categories
from modules import Navbar, Header, AutoRefresh, Footer, Table, SlaBarChart, SlaCardTable



use_case = GetTickets(TicketsRequestsRepository())

st.set_page_config(
    page_title="BI Solicitations",
    page_icon="🧊",
)

def main():
    AutoRefresh()
    Navbar()
    Header()

    st.title("Evolução do SLA")

    departaments = st.multiselect(
        "Escolha os departamentos", categories.keys(),
        placeholder="Selecione um departamento"
    )

    col1, col2 = st.columns([1,1])
    with col1:
        start_date = st.date_input("Data de abertura", None, format="DD/MM/YYYY" )
    with col2:
        close_date = st.date_input("Data de Fechamento", None, format="DD/MM/YYYY")

    if departaments or (start_date and close_date):
        months_sla, sla_exceeded = use_case.sla_per_month(
            departament_selected=departaments,
            start_date=start_date,
            end_date=close_date
        )
    else:
        months_sla, sla_exceeded = use_case.sla_per_month()

    SlaBarChart(months_sla)
    SlaCardTable(months_sla)


    Table(sla_exceeded)

    Footer()

if __name__ == '__main__':
    main()
