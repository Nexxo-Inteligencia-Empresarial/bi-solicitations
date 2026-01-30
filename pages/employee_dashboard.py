import streamlit as st
import pandas as pd

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
    with st.container():
        col1, col2, col3 = st.columns([3, 2, 2])

        employees = [e.upper() for e in use_case.get_employees()]

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

    start_date_filter = (
        start_date.strftime("%Y-%m-%d") if start_date and end_date else None
    )

    end_date_filter = (
        end_date.strftime("%Y-%m-%d") if start_date and end_date else None
    )

    result_data = {}
    if not selected_employees or "TODOS" in selected_employees:
        result_data = use_case.get_tickets(
            employee=None,
            start_date=start_date_filter,
            end_date=end_date_filter
        )
    else:
        for employee in selected_employees:
            data = use_case.get_tickets(
                employee=employee.lower(),
                start_date=start_date_filter,
                end_date=end_date_filter
            )

            for emp, info in data.items():
                if emp not in result_data:
                    result_data[emp] = info
                else:
                    result_data[emp]["solicitações"].extend(info["solicitações"])
                    result_data[emp]["total"] += info["total"]


    rows = []

    for employee, info in result_data.items():
        for ticket in info["solicitações"]:
            row = Mappings.ticket_to_dict(ticket)
            row["Colaborador"] = employee.upper()
            rows.append(row)

    if not rows:
        st.warning("Nenhum resultado encontrado.")
        st.stop()

    df = pd.DataFrame(rows)

    st.markdown("### 📊 Resultados")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


if __name__ == "__main__":
    main()
