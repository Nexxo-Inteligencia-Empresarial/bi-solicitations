from datetime import datetime, date
from collections import defaultdict
from typing import Optional, List, Tuple, Dict
import pytz

import streamlit as st

from src.utils.mappings import Mappings

@st.cache_data
def process_tickets(rows, data_expired, ft_dpt):
    datas = defaultdict(lambda: {"Resolvendo": 0, "Responder": 0, "Atrasadas": 0})

    for status, departament, count in rows:
        departament = Mappings.classify_departaments(departament)

        if departament is None:
            continue

        if not Mappings.filter_departament(departament, ft_dpt):
            continue

        datas[departament][status] += count

    for departament, count_expired in data_expired:
        departament = Mappings.classify_departaments(departament)

        if departament is None:
            continue

        if not Mappings.filter_departament(departament, ft_dpt):
            continue

        resolving_before = datas[departament]["Resolvendo"]
        subtract_amount = min(count_expired, resolving_before)

        datas[departament]["Atrasadas"] += count_expired
        datas[departament]["Resolvendo"] = resolving_before - subtract_amount

    return dict(datas)

@st.cache_data
def process_open_tickets(rows: List[Dict], ft_dpt, ft_stts):
    datas = []
    for row in rows:
        create_date = datetime.fromisoformat(row.get("create_date")).date()

        departament = Mappings.classify_departaments(row.get("departament").lower())

        if departament is None:
            continue

        if not Mappings.filter_departament(departament, ft_dpt):
            continue

        today = date.today()

        due_date = datetime.fromisoformat(row.get("due_date")).date() if row.get("due_date") else None

        if due_date and due_date <  today and row.get('status') == 'Resolvendo':
            row['status'] = "Atrasada"

        if not Mappings.filter_status(row.get('status'), ft_stts):
            continue

        ticket_info = {
            "ID": row.get('ticket_id'),
            "Departamento": departament,
            "Status": row.get('status'),
            "Vencimento": row.get('due_date'),
            "Criação": create_date,
            "Responsável" : row.get('responsible'),
            "Sistema": row.get('system'),
            "Tipo": row.get('type'),
        }

        datas.append(ticket_info)

    return datas

@st.cache_data
def process_sla_per_month(rows: List[Dict], departament_selected, start_date, end_date):
    months_sla  = months_sla = defaultdict(lambda: {"Fora do SLA": 0, "Dentro do SLA": 0})

    for row in rows:

        departament = Mappings.classify_departaments(row.get('departament').lower())

        if departament is None:
            continue

        if not Mappings.filter_departament(departament, departament_selected):
            continue

        conclusion_date = datetime.fromisoformat(row.get('conclusion_date')).date()
        create_date = datetime.fromisoformat(row.get('create_date')).date()


        if start_date and end_date:
            if not Mappings.filter_date(conclusion_date, start_date, end_date):
                continue

        days = (conclusion_date - create_date).days


        month_solicitation = create_date.month

        if days <= 2:
            months_sla[month_solicitation]["Dentro do SLA"] += 1
        else:
            months_sla[month_solicitation]["Fora do SLA"] += 1

    return dict(months_sla)

@st.cache_data
def process_general_sla(rows: List[Dict], departament_selected, start_date, end_date):
        status_totals = {"Dentro do SLA": 0, "Fora do SLA": 0}

        for row in rows:


            departament = Mappings.classify_departaments(row.get('departament').lower())

            if departament is None:
                continue

            if not Mappings.filter_departament(departament, departament_selected):
                continue

            conclusion_date = datetime.fromisoformat(row.get('conclusion_date')).date()
            create_date = datetime.fromisoformat(row.get('create_date')).date()

            if start_date and end_date:
                if not Mappings.filter_date(conclusion_date, start_date, end_date):
                    continue

            days = (conclusion_date - create_date).days


            if days <= 2:
                status_totals["Dentro do SLA"] += 1
            else:
                status_totals["Fora do SLA"] += 1

        labels = list(status_totals.keys())
        values = list(status_totals.values())

        return labels, values

@st.cache_data
def process_exceded_sla(rows: List[Dict], departament_selected, start_date, end_date):
        sla_exceeded = []

        for row in rows:

            departament = Mappings.classify_departaments(row.get('departament').lower())

            if departament is None:
                continue

            if not Mappings.filter_departament(departament, departament_selected):
                continue

            conclusion_date = datetime.fromisoformat(row.get('conclusion_date')).date()
            create_date = datetime.fromisoformat(row.get('create_date')).date()

            if start_date and end_date:
                if not Mappings.filter_date(conclusion_date, start_date, end_date):
                    continue

            days = (conclusion_date - create_date).days

            ticket_info = {
                "ID": row.get('ticket_id'),
                "Departamento": row.get('departament'),
                "Sistema": row.get('system'),
                "Tipo": row.get('type'),
                "Data de criação": create_date,
                "Data de conclusão": conclusion_date,
                "Dias para a conclusão": days,
            }

            if days >= 2:
                sla_exceeded.append(ticket_info)

        return sla_exceeded
