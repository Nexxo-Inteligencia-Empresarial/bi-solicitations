import streamlit as st
import pandas as pd
import plotly.express as px

from src.data.use_cases.get_employees_tickets import GetEmployeetickets
from src.infra.db.repositories.employees_tickets_reporitory import EmployeesTicketsRepository
from modules.nav import Navbar
from src.utils.mappings import Mappings

use_case = GetEmployeetickets(EmployeesTicketsRepository())

st.set_page_config(
    page_title="Solicitações Respondidas",
    layout="wide"
)


def main():
    Navbar()

    st.title("📋 Solicitações Respondidas por Funcionário")
    # -----------------------------
    # FILTOS E MENUS
    # -----------------------------

    with st.container():
        col1, col2, col3 = st.columns([3, 2, 2])

        employees = pd.Series(use_case.get_employees()).str.upper().tolist()

        with col1:
            selected_employees = st.multiselect(
                "Funcionários",
                employees
            )

        with col2:
            start_date = st.date_input(
                "Data inicial",
                format="DD/MM/YYYY"
            )

        with col3:
            end_date = st.date_input(
                "Data final",
                format="DD/MM/YYYY"
            )

    with st.container():
        col1, col2, col3 = st.columns([1, 2, 2])

        with col1:
            SYSTEMS = ["onvio", "acessórias"]
            system = st.multiselect(
                "Sistema",
                SYSTEMS,
                default=SYSTEMS
            )


    start_date_filter = (
        start_date.strftime("%Y-%m-%d") if start_date and end_date else None
    )

    end_date_filter = (
        end_date.strftime("%Y-%m-%d") if start_date and end_date else None
    )

    if not selected_employees:
        result_data = use_case.get_tickets(
            employee=None,
            start_date=start_date_filter,
            end_date=end_date_filter
        )

    else:
        result_data = {}

        for employee in selected_employees:
            data = use_case.get_tickets(
                employee=employee.lower(),
                start_date=start_date_filter,
                end_date=end_date_filter
            )

            result_data.update(data)


    # -----------------------------
    # RESULT_DATA → DATAFRAME
    # -----------------------------
    dfs = [
        pd.DataFrame(
            (Mappings.ticket_to_dict(ticket) for ticket in info["solicitações"])
        ).assign(Colaborador=employee.upper())

        for employee, info in result_data.items()
        if info["solicitações"]
    ]

    if not dfs:
        st.warning("Nenhum resultado encontrado.")
        st.stop()

    df = pd.concat(dfs, ignore_index=True)

    table_df = (
        df[df["Sistema"].isin(system)]
    )

    chart_df = (
        df[df["Sistema"].isin(system)]  # <- filtro
        .groupby("Colaborador")
        .size()
        .reset_index(name="Solicitações")
        .sort_values(by="Solicitações", ascending=True)
    )


    # -----------------------------
    ## GRAPHS AND DATAFRAMES
    # -----------------------------

    fig = px.bar(
    chart_df,
    x="Solicitações",
    y="Colaborador",
    orientation="h",
    text="Solicitações",
    )
    fig.update_traces(textposition="outside", cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True)
    fig.update_yaxes(
        tickmode="linear"    )

    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True
    )


if __name__ == "__main__":
    main()
