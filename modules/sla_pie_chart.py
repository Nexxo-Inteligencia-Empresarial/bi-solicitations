import streamlit as st
import plotly.graph_objects as go
from uuid import uuid4

from src.data.use_cases.interface.get_tickets import GetTickets

class SlaPieChart():

    def __init__(self, use_case: GetTickets, ft_dpt, start_date, close_date):
        datas = use_case.get_sla(ft_dpt, start_date, close_date)
        self.__render(datas)

    def __render(self, datas):
        labels, values = datas
        colors = ["#3b7c59" if label != "Fora do SLA" else '#EE0000' for label in labels]

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker_colors=colors,
            textinfo='percent',
            hoverinfo='label+value',
            textfont_size=15,
            textfont=dict(size=12, color='white'),
            insidetextorientation='auto'
        )])

        fig.update_layout(
            height=400,
            margin=dict(t=100, b=5, l=20, r=20),
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True, key=f"plot_{uuid4()}")
