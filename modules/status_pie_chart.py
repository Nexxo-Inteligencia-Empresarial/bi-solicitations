import plotly.graph_objects as go
from uuid import uuid4
import streamlit as st

from src.utils.mappings import Mappings
from src.data.use_cases.interface.get_tickets import GetTickets

class StatusPieChart:

    def __init__(self, use_case: GetTickets, ft_dpt):
        datas = use_case.get_open_tickets(ft_dpt,total=True)
        self.__render(datas)

    def __render(self, datas):

        renamed_datas = {
            Mappings.status(status): qty
            for status, qty in datas.items()
        }

        labels = list(renamed_datas.keys())
        values = list(renamed_datas.values())

        colors = [Mappings.color(label) for label in labels]

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker_colors=colors,
            textinfo='percent',
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
