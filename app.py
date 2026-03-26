import streamlit as st

from src.data.use_cases.get_tickets import GetTickets as Dataset
from src.data.use_cases.get_last_executation import GetLastExecution as DatasetExecution
from src.infra.db.repositories.execution_collection_repository import ExecutionCollectionRepository
from src.infra.db.repositories.tickets_requests_repository import TicketsRequestsRepository
from modules import Navbar, Header, AutoRefresh, Footer, StatusBarChart, StatusPieChart, TableSolicitations, AlertOutdate
from src.utils.map_departaments import departaments


dataset = Dataset(TicketsRequestsRepository())
dataset_execution = DatasetExecution(ExecutionCollectionRepository())

st.set_page_config(
    page_title="BI Solicitations",
    page_icon="🧊",
)

st.logo(image='images/logo.png')

def main():
    AlertOutdate(dataset_execution.get())
    AutoRefresh()
    Navbar()
    Header()
    ft_dpt = st.multiselect(
        "Filtro por departamentos", departaments.keys(),
        placeholder="Selecione um departamento"
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        data = dataset.get_by_departament(ft_dpt)
        StatusBarChart(data)

    with col2:
        StatusPieChart(dataset.get_open_tickets(ft_dpt,total=True))
        col1, col2 = st.columns([1,1])

    ft_stts_row =  st.columns(3)
    with ft_stts_row[0]:
        ft_stts = st.multiselect(
            "Filtro por status", ["Responder", "Resolvendo", "Atrasada"],
            placeholder="Selecione um Status"
        )

    TableSolicitations(dataset.get_open_tickets(ft_dpt, ft_stts))

    for system, last_execution in dataset_execution.get():
        st.markdown(f"""
            <div style="text-align: center; font-size: 16px;">
                <strong>{system.capitalize()}</strong>: {last_execution.strftime('%d/%m/%Y %H:%M:%S')}
            </div>
        """, unsafe_allow_html=True)

    Footer()

if __name__ == '__main__':
    main()
