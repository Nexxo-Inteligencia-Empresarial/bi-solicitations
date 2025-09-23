from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st

class AlertOutdate:
    def __init__(self, last_execution_datas: list):
        self.__render(last_execution_datas)

    def __render(self, last_execution_datas: list):
        # Define fuso horário do Brasil
        now = datetime.now(ZoneInfo("America/Sao_Paulo"))

        for system, last_execution in last_execution_datas:
            # Se last_execution não tiver timezone, é bom ajustar
            if last_execution.tzinfo is None:
                last_execution = last_execution.replace(tzinfo=ZoneInfo("America/Sao_Paulo"))

            elapsed_time = now - last_execution
            minutes_passed = elapsed_time.total_seconds() / 60

            if minutes_passed >= 45:
                st.warning(f"Coleta do sistema {system} está desatualizada", icon="⚠️")
