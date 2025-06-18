import streamlit as st
import plotly.graph_objects as go
from uuid import uuid4
from src.data.use_cases.get_tickets import GetTickets
from src.infra.db.repositories.tickets_requests_repository import TicketsRequestsRepository
from src.utils.map_categories import categories
from modules import Navbar, Header, AutoRefresh, Footer



use_case = GetTickets(TicketsRequestsRepository())

st.set_page_config(
    page_title="BI Solicitations",
    page_icon="🧊",
)
  
def main():
    AutoRefresh()
    Navbar()
    Header()
    
    st.title("SLA")
    
    departaments = st.multiselect(
        "Escolha os departamentos", categories.keys(),
        placeholder="Selecione um departamento"
    )
    
    col1, col2 = st.columns([1,1])
    with col1:
        start_date = st.date_input("Data de abertura", None)
    with col2:
        close_date = st.date_input("Data de Fechamento", None)

    if departaments or (start_date and close_date):
        labels, values = use_case.get_tickets_dates_filters(
                        departament_selected=departaments,
                        start_date=start_date,
                        end_date=close_date
                    )
    else:
        labels, values = use_case.get_tickets_dates()
            
    colors = ["#3b7c59" if label != "Fora do SLA" else '#EE0000' for label in labels]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker_colors=colors,
        textinfo='label+value',
        textfont_size=18,
        textfont=dict(size=18, color='white'),
        insidetextorientation='auto'
    )])

    fig.update_layout(
        height=700,
        margin=dict(t=100, b=5, l=20, r=20),
        legend=dict(font=dict(size=16))
    )

    st.plotly_chart(fig, use_container_width=True, key=f"plot_{uuid4()}")

    Footer()

if __name__ == '__main__':
    main()
