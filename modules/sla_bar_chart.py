import streamlit as st
import plotly.graph_objects as go

from src.utils.mappings import Mappings
from src.data.use_cases.interface.get_tickets import GetTickets

class SlaBarChart:

    def __init__(self, use_case: GetTickets, ft_dpt, start_date, end_date):
        datas = use_case.sla_per_month(ft_dpt, start_date, end_date)
        self.__render(datas)

    def __render(self, datas):
        meses = sorted(datas.keys())

        dentro_sla_percent = []
        fora_sla_percent = []

        for m in meses:
            dentro = datas[m]["Dentro do SLA"]
            fora = datas[m]["Fora do SLA"]
            total = dentro + fora

            if total > 0:
                dentro_sla_percent.append((dentro / total) * 100)
                fora_sla_percent.append((fora / total) * 100)
            else:
                dentro_sla_percent.append(0)
                fora_sla_percent.append(0)

        meses_labels = [Mappings.months(m) for m in meses]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=meses_labels,
            y=dentro_sla_percent,
            name="Dentro do SLA",
            marker_color="#3b7c59",
            text=[f"{v:.1f}%" for v in dentro_sla_percent],
            textposition="inside",
            insidetextanchor="middle"
        ))

        fig.add_trace(go.Bar(
            x=meses_labels,
            y=fora_sla_percent,
            name="Fora do SLA",
            marker_color="red",
            text=[f"{v:.1f}%" for v in fora_sla_percent],
            textposition="inside",
            insidetextanchor="middle"
        ))

        fig.update_layout(
                barmode="stack",
                xaxis_title="Mês",
                yaxis_title=None,
                legend_title="Status SLA",
                height=500,

                font=dict(size=14, family="Arial", color="#444"),
                yaxis=dict(
                    range=[0, 100],
                    showticklabels=False,
                    showgrid=False
                )
            )

        fig.update_traces(
            marker_line_width=0.5,
            marker_line_color="rgba(0,0,0,0.1)",
            width=0.5,
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
