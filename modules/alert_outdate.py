from datetime import datetime
import streamlit as st

class  AlertOutdate():

    def __init__(self, last_execution_datas: dict):
        self.__render(last_execution_datas)

    def __render(self, last_execution_datas):
        today = datetime.now()
        for system , last_execution in last_execution_datas:
            last_execution = last_execution
            days = (today - last_execution).days

            if days >= 1 :
                st.warning(f"Coleta do sistema {system} está desatualizada ", icon='⚠️', )
