import pandas as pd
import altair as alt
import streamlit as st

class StatusBarChart:

    def __init__(self, data_items: list):
        self.__render(data_items)

    def __render(self, data_items: list):
        df = self.__create_combined_dataframe(data_items)
        chart = self.__create_stacked_bar_chart(df)
        st.altair_chart(chart, use_container_width=True)

    def __create_combined_dataframe(self, data_items: list) -> pd.DataFrame:
        records = []
        for department, values in data_items:
            for status, qty in values.items():
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
            y=alt.Y("Departamento:N", sort='-x', title=None, axis=alt.Axis(labelFontSize=18,
                                                                            labelColor="#31333F",
                                                                            labelLimit=0,
                                                                            labelPadding=10,
                                                                            labelFontWeight='bolder')),
            x=alt.X("Quantidade:Q", title="Quantidade", scale=alt.Scale(domain=[0, limit])),
            color=alt.Color(
                "Status:N",
                scale=alt.Scale(
                    domain=["Responder", "Resolvendo", "Atrasadas"],
                    range=["#2d95ec", "#f6ba2a", "#e23512"]
                ),
                legend=alt.Legend(title="Status")
            ),
            tooltip=["Departamento:N", "Status:N", "Quantidade:Q"]
        ).properties(
            width=700,
            height=700,
            title="Solicitações por Departamento e Status"
        ).configure_axis(
            labelFontSize=14,
            titleFontSize=14,
            grid=False
        ).configure_view(
            stroke=None
        )

        return chart
