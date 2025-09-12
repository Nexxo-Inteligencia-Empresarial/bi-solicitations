from datetime import datetime, date
from collections import defaultdict
from typing import Optional, List, Tuple
import pytz

from src.infra.db.interfaces.tickets_requests_repository import TicketsRequestsRepositoryInterface
from src.utils.map_categories import categories
from src.utils.map_months import MapMonths

class GetTickets:
    def __init__(self, tickets_requests_repository: TicketsRequestsRepositoryInterface):
        self.tickets_requests_repository = tickets_requests_repository

    def get(self):

        brazil_timezone = pytz.timezone('America/Sao_Paulo')
        now_brazil = datetime.now(brazil_timezone)
        today = now_brazil.isoformat()

        rows = self.tickets_requests_repository.get_tickets_departaments(today)

        status_totals = {"Resolvendo": 0, "Responder": 0}

        for status, departament, count in rows:
            category = self.__classify_departaments(departament)

            if category is None:
                continue

            if status in status_totals:
                status_totals[status] += count

        labels = list(status_totals.keys())
        values = list(status_totals.values())
        return labels, values

    def get_full(self, ft_dpt:Optional[List[str]] = None, ft_stts:Optional[List[str]] = None):
        brazil_timezone = pytz.timezone('America/Sao_Paulo')
        now_brazil = datetime.now(brazil_timezone).date()

        today = now_brazil.isoformat()

        rows = self.tickets_requests_repository.get_tickets_full(today)
        datas = []
        for row in rows:
            create_date = datetime.fromisoformat(row.create_date).date()

            category = self.__classify_departaments(row.departament.lower())

            if not self.__filter_departament(category, ft_dpt):
                continue

            today = date.today()

            due_date = datetime.fromisoformat(row.due_date).date() if row.due_date else None

            if due_date and due_date <  today :
                row.status = "Atrasada"

            if not self.__filter_status(row.status, ft_stts):
                continue

            ticket_info = {
                "ID": row.ticket_id,
                "Departamento": category,
                "Status": row.status,
                "Vencimento": row.due_date,
                "Criação": create_date,
                "Responsável" : row.responsible,
                "Sistema": row.system,
                "Tipo": row.type,
            }

            datas.append(ticket_info)

        return datas



    def get_by_departament(self):
        brazil_timezone = pytz.timezone('America/Sao_Paulo')
        now_brazil = datetime.now(brazil_timezone).date()

        today = now_brazil.isoformat()

        rows = self.tickets_requests_repository.get_tickets_departaments(today)
        data_expired = self.tickets_requests_repository.get_tickets_expired(today)
        datas = defaultdict(lambda: {"Resolvendo": 0, "Responder": 0, "Atrasadas": 0})
        for status, departament, count in rows:
            category = self.__classify_departaments(departament)
            if category is None:
                continue
            datas[category][status] += count

        for departament, count_expired in data_expired:
            category = self.__classify_departaments(departament)
            if category is None:
                continue

            resolving_before = datas[category]["Resolvendo"]
            subtract_amount = min(count_expired, resolving_before)

            datas[category]["Atrasadas"] = datas[category]["Atrasadas"] + count_expired
            datas[category]["Resolvendo"] = resolving_before - subtract_amount

        return dict(datas)

    def get_tickets_dates(self):
        data = self.tickets_requests_repository.get_tickets_dates()
        status_totals = {"Dentro do SLA": 0, "Fora do SLA": 0}
        fora_sla = []

        for row in data:
            conclusion_date = datetime.fromisoformat(row.conclusion_date).date()
            create_date = datetime.fromisoformat(row.create_date).date()
            dias = (conclusion_date - create_date).days

            ticket_info = {
                "ticket_id": row.ticket_id,
                "departament": row.departament,
                "system": row.system,
                "type": row.type,
                "create_date": create_date,
                "conclusion_date": conclusion_date,
                "days_to_conclusion": dias,
            }

            if dias <= 2:
                status_totals["Dentro do SLA"] += 1
            else:
                status_totals["Fora do SLA"] += 1
                fora_sla.append(ticket_info)

        labels = list(status_totals.keys())
        values = list(status_totals.values())

        return labels, values, fora_sla

    def sla_per_month(self, departament_selected: Optional[List[str]] = None, start_date: Optional[date] = None, end_date: Optional[date] = None) -> Tuple[List[str], List[int]]:
        data = self.tickets_requests_repository.get_tickets_dates()
        months_sla  = months_sla = defaultdict(lambda: {"Fora do SLA": 0, "Dentro do SLA": 0})

        sla_exceeded = []

        for row in data:

            departament = self.__classify_departaments(row.departament.lower())
            if not self.__filter_departament(departament, departament_selected):
                continue

            conclusion_date = datetime.fromisoformat(row.conclusion_date).date()
            create_date = datetime.fromisoformat(row.create_date).date()


            if start_date and end_date:
                if not self.__filter_date(conclusion_date, start_date, end_date):
                    continue

            days = (conclusion_date - create_date).days

            ticket_info = {
                "ticket_id": row.ticket_id,
                "departament": row.departament,
                "system": row.system,
                "type": row.type,
                "create_date": create_date,
                "conclusion_date": conclusion_date,
                "days_to_conclusion": days,
            }

            month_solicitation = create_date.month

            if days <= 2:
                months_sla[month_solicitation]["Dentro do SLA"] += 1
            else:
                months_sla[month_solicitation]["Fora do SLA"] += 1
                sla_exceeded.append(ticket_info)

        return dict(months_sla), sla_exceeded

    def get_tickets_dates_filters(self, departament_selected: Optional[List[str]] = None, start_date: Optional[date] = None, end_date: Optional[date] = None) -> Tuple[List[str], List[int]]:
        data = self.tickets_requests_repository.get_tickets_dates()
        status_totals = {"Dentro do SLA": 0, "Fora do SLA": 0}
        sla_exceeded = []

        for row in data:


            departament = self.__classify_departaments(row.departament.lower())
            if not self.__filter_departament(departament, departament_selected):
                continue

            conclusion_date = datetime.fromisoformat(row.conclusion_date).date()
            create_date = datetime.fromisoformat(row.create_date).date()

            if start_date and end_date:
                if not self.__filter_date(conclusion_date, start_date, end_date):
                    continue

            days = (conclusion_date - create_date).days

            ticket_info = {
                "ticket_id": row.ticket_id,
                "departament": row.departament,
                "system": row.system,
                "type": row.type,
                "create_date": create_date,
                "conclusion_date": conclusion_date,
                "days_to_conclusion": days,
            }

            if days <= 2:
                status_totals["Dentro do SLA"] += 1
            else:
                status_totals["Fora do SLA"] += 1
                sla_exceeded.append(ticket_info)

        labels = list(status_totals.keys())
        values = list(status_totals.values())

        return labels, values, sla_exceeded

    def __filter_departament(self, departament: str, selected: Optional[List[str]]) -> bool:
        if selected is None or not selected:
            return True
        return departament in selected

    def __filter_status(self, status: str, selected: Optional[List[str]]) -> bool:
        if selected is None or not selected:
            return True
        return status in selected

    def __filter_date(self, conclusion_date: date, start: Optional[date], end: Optional[date]) -> bool:
        if start and conclusion_date < start:
            return False
        if end and conclusion_date > end:
            return False
        return True

    def __classify_departaments(self, departament):
        for category, rules in categories.items():
            if departament in rules:
                return category
        return None
