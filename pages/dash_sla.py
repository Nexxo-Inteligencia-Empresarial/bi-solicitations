import streamlit as st

from src.data.use_cases.get_tickets import GetTickets
from src.infra.db.repositories.tickets_requests_repository import TicketsRequestsRepository
from src.utils.map_categories import categories
from modules import Navbar, Header, AutoRefresh, Footer, TableSlaExceded, SlaPieChart, SlaBarChart, SlaCardTable



use_case = GetTickets(TicketsRequestsRepository())

st.set_page_config(
    page_title="BI Solicitations",
    page_icon="🧊",
)

st.logo(image='images/logo.png')

def main():
    AutoRefresh()
    Navbar()
    Header()

    st.title("SLA")

    ft_dpt = st.multiselect(
        "Escolha os departamentos", categories.keys(),
        placeholder="Selecione um departamento"
    )

    col1, col2 = st.columns([1,1])
    with col1:
        start_date = st.date_input("Data de abertura", None, format="DD/MM/YYYY" )
    with col2:
        close_date = st.date_input("Data de Fechamento", None, format="DD/MM/YYYY")

    render(use_case, ft_dpt, start_date, close_date)

    Footer()

@st.cache_resource
def render(_use_case, ft_dpt, start_date, close_date):
    col_graph1, col_graph2 = st.columns([2, 1])

    with col_graph1:
        SlaBarChart(_use_case, ft_dpt, start_date, close_date)

    with col_graph2:
        SlaPieChart(use_case, ft_dpt, start_date, close_date)

    SlaCardTable(use_case, ft_dpt, start_date, close_date)
    TableSlaExceded(use_case, ft_dpt, start_date, close_date)

if __name__ == '__main__':
    main()
