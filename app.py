from streamlit_autorefresh import st_autorefresh
import streamlit as st
import plotly.graph_objects as go
import time

from src.data.use_cases.get_tickets import GetTickets
from src.infra.db.repositories.tickets_requests_repository import TicketsRequestsRepository

use_case = GetTickets(TicketsRequestsRepository())

st.set_page_config(
    page_title="BI Solicitations",
    page_icon="🧊",
)

count = st_autorefresh(interval=600000)

st.markdown("""
    <style>
        #MainMenu, header, footer { visibility: hidden; }
        .main { padding-left: 0rem; padding-right: 0rem; }
        .block-container {
            padding-left: 10rem;
            padding-right: 10rem;
            padding-top: 0;
            padding-bottom: 1rem;
            margin: 0;
            max-width: 100%;
        }
        body { margin: 0; padding: 0; overflow-x: hidden; }
        h1 { margin-top: 0rem; font-size: 40px; }
    </style>
""", unsafe_allow_html=True)

if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()
if "refresh_interval" not in st.session_state:
    st.session_state.refresh_interval = 3600

st.title("Solicitações")

labels, values = use_case.get()
colors = ['#3b7c59' if label != "Responder" else '#EE0000' for label in labels]

fig = go.Figure(data=[go.Pie(
    labels=labels,
    values=values,
    marker_colors=colors,
    textinfo='label+value',
    textfont_size=18,
    insidetextorientation='auto'
)])

fig.update_layout(
    height=700,
    margin=dict(t=100, b=5, l=20, r=20),
    legend=dict(font=dict(size=16))
)

st.plotly_chart(fig, use_container_width=True, key=f"plot_{int(st.session_state.last_update)}")

st.markdown("""
    <div style="text-align: right; opacity: 0.6; font-size: 18px;">
        <b>Hubnexxo</b> | Soluções Empresariais
    </div>
""", unsafe_allow_html=True)

if time.time() - st.session_state.last_update > st.session_state.refresh_interval:
    st.session_state.last_update = time.time()
    st.experimental_rerun()
