import streamlit as st

from src.data.use_cases.get_tickets import GetTickets as Dataset
from src.infra.db.repositories.tickets_requests_repository import TicketsRequestsRepository
from src.utils.map_departaments import departaments
from modules import Navbar, Header, AutoRefresh, Footer, TableSolicitations


dataset = Dataset(TicketsRequestsRepository())

st.set_page_config(
    page_title="BI Solicitations - Renegociações",
    page_icon="🧊",
)

st.logo(image='images/logo.png')


def main():
    AutoRefresh()
    Navbar()
    Header()

    st.title("Solicitações com Renegociações")

    ft_dpt = st.multiselect(
        "Filtro por departamentos", departaments.keys(),
        placeholder="Selecione um departamento"
    )

    render(ft_dpt)
    Footer()


@st.cache_resource
def render(ft_dpt):
    data = dataset.get_with_renegotiations(ft_dpt, [])

    st.markdown(f"### Total de solicitações: **{len(data)}**")

    grouped = group_by_status(data)

    with st.expander(f"Responder ({len(grouped.get('Responder', []))})", expanded=True):
        TableSolicitations(grouped.get('Responder', []))

    with st.expander(f"Resolvendo ({len(grouped.get('Resolvendo', []))})"):
        TableSolicitations(grouped.get('Resolvendo', []))

    with st.expander(f"Respondida ({len(grouped.get('Respondida', []))})"):
        responded_rows = [
            {k: v for k, v in row.items() if k != "Vencimento"}
            for row in grouped.get('Respondida', [])
        ]
        TableSolicitations(responded_rows)


def group_by_status(rows):
    grouped = {'Responder': [], 'Resolvendo': [], 'Respondida': []}

    for row in rows:
        status = row.get('Status')

        if status not in grouped:
            continue

        grouped[status].append(row)

    return grouped


if __name__ == '__main__':
    main()
