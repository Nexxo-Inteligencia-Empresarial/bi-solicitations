import streamlit as st
import plotly.graph_objects as go
import time

from src.data.use_cases.get_tickets import GetTickets
from src.infra.db.repositories.tickets_requests_repository import TicketsRequestsRepository

use_case = GetTickets(TicketsRequestsRepository())
labels, values = use_case.get()


st.markdown("""
    <style>
        /* Remove menu, header e footer padrão */
        #MainMenu, header, footer {
            visibility: hidden;
        }

        /* Ocupa toda a largura e altura */
        .main {
            padding-left: 0rem;
            padding-right: 0rem;
        }

        .block-container {
            padding-left: 10rem;
            padding-right: 10rem;
            padding-top: 1rem;
            padding-bottom: 1rem;
            margin: 0;
            max-width: 100%;
        }

        body {
            margin: 0;
            padding: 0;
            overflow-x: hidden;
        }

        /* Título sem margem superior exagerada */
        h1 {
            margin-top: 0rem;
            font-size: 40px;
        }
    </style>
""", unsafe_allow_html=True)

# Configuração de sessão para controle de tempo
if 'last_run' not in st.session_state:
    st.session_state.last_run = time.time()


# Gráfico de pizza com labels e valores maiores
st.title("Solicitações")

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    textinfo='label+value',
    textfont_size=18,
    insidetextorientation='auto'
)])

fig.update_layout(
    height=700,  # Aumenta a altura do gráfico
    margin=dict(t=80, b=5, l=20, r=20),
    legend=dict(
        font=dict(size=16)  # Tamanho maior da legenda
    )
)

st.plotly_chart(fig, use_container_width=True)

# Rodapé com branding
st.markdown("""
    <div style="text-align: right; opacity: 0.6; font-size: 18px;">
        <b>Hubnexxo</b> | Soluções Empresariais
    </div>
""", unsafe_allow_html=True)

now = time.time()
if now - st.session_state.last_run > 3600:
    st.session_state.last_run = now
    st.experimental_rerun()
