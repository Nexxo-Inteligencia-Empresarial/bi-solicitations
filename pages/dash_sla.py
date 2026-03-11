import streamlit as st

from src.data.use_cases.get_tickets_sla import GetTicketsSla as Dataset
from src.infra.db.repositories.tickets_requests_repository import TicketsRequestsRepository
from src.utils.map_categories import categories
from modules import Navbar, Header, AutoRefresh, Footer, TableSlaExceded, SlaPieChart, SlaBarChart, SlaCardTable



dataset = Dataset(TicketsRequestsRepository())

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

    render(ft_dpt, start_date, close_date)

    Footer()

@st.cache_resource
def render(ft_dpt, start_date, close_date):
    col_graph1, col_graph2 = st.columns([2, 1])

    dataset.set_dataset(start_date, close_date)

    with col_graph1:
        SlaBarChart(dataset.sla_per_month(ft_dpt))

    with col_graph2:
        SlaPieChart(dataset.get_sla(ft_dpt))

    SlaCardTable(dataset.sla_per_month(ft_dpt))
    TableSlaExceded(dataset.get_sla_exceded(ft_dpt))

if __name__ == '__main__':
    main()
