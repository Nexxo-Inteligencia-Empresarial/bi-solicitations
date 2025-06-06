from streamlit_autorefresh import st_autorefresh
import streamlit as st
import pandas as pd
import altair as alt

from src.data.use_cases.get_tickets import GetTickets
from src.infra.db.repositories.tickets_requests_repository import TicketsRequestsRepository

def get_status_image_path(responder_qtd):
    if responder_qtd == 0:
        return "images/status_baixo.png"
    elif responder_qtd <= 10:
        return "images/status_medio.png"
    else:
        return "images/status_alto.png"

st.set_page_config(layout="wide", page_title="BI Solicitations", page_icon="🧊")

count = st_autorefresh(interval=600000)

use_case = GetTickets(TicketsRequestsRepository())
datas = use_case.get_by_departament()

total_solicitations = sum(sum(status_qtd.values()) for status_qtd in datas.values())

st.markdown("<h1 style='text-align: center; margin-bottom: 10px'>Solicitações Abertas Acessórias/Onvio</h1>", unsafe_allow_html=True)

st.markdown(
    f"<h3 style='text-align: center; color: #444; font-weight: normal;'>Total de solicitações: <strong>{total_solicitations}</strong></h3>",
    unsafe_allow_html=True
)

datas_itens = list(datas.items())
datas_itens.sort(key=lambda item: sum(item[1].values()), reverse=True)

for i in range(0, len(datas_itens), 3):
    row = datas_itens[i:i+3]
    cols = st.columns([1, 1, 1])

    for col, (setor, values) in zip(cols, row):
        total = sum(values.values())
        df = pd.DataFrame({
            "Status": list(values.keys()),
            "Quantidade": list(values.values())
        })

        with col:
            header_col1, header_col2 = st.columns([6, 1])
            with header_col1:
                st.markdown(f"### {setor}")
            # with header_col2:
            #     responder_qtd = values.get("Responder", 0)
            #     img_path = get_status_image_path(responder_qtd)
            #     st.image(img_path, width=30)

            st.markdown(f"Total de solicitações: **{total}**")

            max_val = df["Quantidade"].max()
            limit = int(max_val * 1.1)

            base = alt.Chart(df).encode(
                y=alt.Y("Status", title=None),
                x=alt.X("Quantidade", title=None, axis=None, scale=alt.Scale(domain=[0, limit]))
            )

            bars = base.mark_bar(size=25).encode(
            color=alt.Color('Status:N', scale=alt.Scale(domain=['Responder', 'Resolvendo'], range=['#EE0000', '#eec50c']), legend=None)
            )

            text = base.mark_text(
                align="left",
                baseline="middle",
                dx=1,
                color="black",
                fontSize=13
            ).encode(
                text="Quantidade"
            )

            chart = (bars + text).properties(
                width=350,
                height=120,
            ).configure_axis(
                labelColor="black",
                domain=False,
                grid=False,
                labelFontWeight='normal',
                labelFontSize=15
            ).configure_view(
                stroke=None
            )

            st.altair_chart(chart, use_container_width=False)

st.markdown("""
    <div style="text-align: right; opacity: 0.6; font-size: 18px;">
        <b>Hubnexxo</b> | Soluções Empresariais
    </div>
""", unsafe_allow_html=True)
