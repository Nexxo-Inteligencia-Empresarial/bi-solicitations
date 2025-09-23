from datetime import datetime
import streamlit as st

class  AlertOutdate():

    def __init__(self, last_execution_datas: dict):
        self.__render(last_execution_datas)

    def __render(self, last_execution_datas):
        now = datetime.now()
        for system, last_execution in last_execution_datas:
            elapsed_time = now - last_execution
            minutes_passed = elapsed_time.total_seconds() / 60

            if minutes_passed >= 45:
                st.warning(f"Coleta do sistema {system} está desatualizada", icon='⚠️')
