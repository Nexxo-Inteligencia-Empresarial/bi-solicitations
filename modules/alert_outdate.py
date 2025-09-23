import streamlit as st
from datetime import datetime

class AlertOutdate:
    def __init__(self, last_execution_datas: list):
        self.__render(last_execution_datas)

    def __render(self, last_execution_datas: list):
        now = datetime.now()
        for system, last_execution in last_execution_datas:
            elapsed_time = now - last_execution
            minutes_passed = elapsed_time.total_seconds() / 60

            if minutes_passed >= 45:
                st.warning(f"Coleta do sistema {system} está desatualizada", icon="⚠️")
