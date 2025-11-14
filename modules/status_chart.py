import pandas as pd
import altair as alt
import streamlit as st

from src.utils.mappings import Mappings

class StatusChart:

    def __init__(self, data_items: list):
        self.__render(data_items)

    def __render(self, data_items: list):
        for i in range(0, len(data_items), 3):
            row = data_items[i:i+3]
            cols = st.columns([1, 1, 1])
            for col, (department, values) in zip(cols, row):
                self.__render_department(col, department, values)

    def __render_department(self, col, department: str, values: dict):
        total = sum(values.values())
        df = self.__create_status_dataframe(values)

        with col:
            header_col1, _ = st.columns([6, 1])
            with header_col1:
                st.markdown(f"### {department}")

            st.markdown(f"Total requests: **{total}**")

            chart = self.__create_status_chart(df)
            st.altair_chart(chart, use_container_width=False)

    def __create_status_dataframe(self, values: dict) -> pd.DataFrame:

        new_values = {
            Mappings.status(k): v for k, v in values.items()
        }

        return pd.DataFrame({
            "Status": list(new_values.keys()),
            "Quantity": list(new_values.values())
        })

    def __create_status_chart(self, df: pd.DataFrame) -> alt.Chart:
        max_val = df["Quantity"].max()
        limit = int(max_val * 1.1)

        base = alt.Chart(df).encode(
            y=alt.Y("Status", title=None),
            x=alt.X("Quantity", title=None, axis=None, scale=alt.Scale(domain=[0, limit]))
        )

        bars = base.mark_bar(size=25).encode(
            color=alt.Color(
                'Status:N',
                scale=alt.Scale(
                    domain=['Sem Análise', 'Resolvendo', 'Atrasadas'],
                    range=["#2d95ec", "#f6ba2a", "#e23512"]
                ),
                legend=None
            )
        )

        text = base.mark_text(
            align="left",
            baseline="middle",
            dx=1,
            color="black",
            fontSize=13
        ).encode(
            text="Quantity"
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

        return chart
