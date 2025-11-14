import pandas as pd
import altair as alt
import streamlit as st

from src.utils.mappings import Mappings
from src.data.use_cases.interface.get_tickets import GetTickets

class StatusBarChart:

    def __init__(self, use_case: GetTickets, ft_dpt):
        datas = use_case.get_by_departament(ft_dpt)
        self.__render(datas)

    def __render(self,datas):
        datas = self.__process_datas(datas)
        if datas:
            df = self.__create_combined_dataframe(datas)
            chart = self.__create_stacked_bar_chart(df)
            st.altair_chart(chart, use_container_width=True)

    def __create_combined_dataframe(self, datas: list) -> pd.DataFrame:
        records = []
        for department, values in datas:
            for status, qty in values.items():
                status = Mappings.status(status)
                records.append({
                    "Departamento": department,
                    "Status": status,
                    "Quantidade": qty
                })
        return pd.DataFrame(records)

    def __create_stacked_bar_chart(self, df: pd.DataFrame) -> alt.Chart:
        max_val = df.groupby("Departamento")["Quantidade"].sum().max()
        limit = int(max_val * 1.1)

        chart = alt.Chart(df).mark_bar(size=37).encode(
            y=alt.Y("Departamento:N", sort='-x', title=None, axis=alt.Axis(labelFontSize=15,
                                                                            labelColor="#31333F",
                                                                            labelLimit=0,
                                                                            labelPadding=10,
                                                                            )),
            x=alt.X("Quantidade:Q", title="Quantidade", scale=alt.Scale(domain=[0, limit])),
            color=alt.Color(
                "Status:N",
                scale=alt.Scale(
                    domain=["Sem Análise", "Resolvendo", "Atrasadas"],
                    range=["#2d95ec", "#f6ba2a", "#e23512"]
                ),
                legend=alt.Legend(title="Status")
            ),
            tooltip=["Departamento:N", "Status:N", "Quantidade:Q"]
        ).properties(
            width=700,
            height=550,
        ).configure_axis(
            labelFontSize=14,
            titleFontSize=14,
            grid=False
        ).configure_view(
            stroke=None
        )

        return chart

    def __process_datas(self, datas):
        datas_itens = list(datas.items())
        datas_itens.sort(key=lambda item: sum(item[1].values()), reverse=True)
        return datas_itens
