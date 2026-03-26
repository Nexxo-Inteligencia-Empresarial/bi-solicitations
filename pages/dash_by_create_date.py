import streamlit as st

from src.data.use_cases.get_tickets import GetTickets as Dataset
from src.infra.db.repositories.tickets_requests_repository import TicketsRequestsRepository
from src.utils.map_departaments import departaments
from src.utils.mappings import Mappings
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

    ft_dpt = st.multiselect(
        "Escolha os departamentos", departaments.keys(),
        placeholder="Selecione um departamento"
    )

    col1, col2 = st.columns([1,1])


    with col1:
        start_date = st.date_input("Data de abertura", None, format="DD/MM/YYYY" )
    with col2:
        close_date = st.date_input("Data de Fechamento", None, format="DD/MM/YYYY")
    categories_options = Mappings.categories()
    categories =  st.multiselect("Cateogrias", categories_options, default=categories_options)

    render(ft_dpt, start_date, close_date, categories)
    Footer()

@st.cache_resource
def render(ft_dpt, start_date, close_date, categories):
    datas = dataset.get_by_create_date(ft_dpt,start_date,close_date,categories)
    st.metric("Quantidade de solicitações", len(datas))
    st.dataframe(datas)

if __name__ == '__main__':
    main()
