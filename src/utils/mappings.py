from typing import Optional, List, Tuple
from .map_categories import categories
from datetime import date

class Mappings:

    @classmethod
    def months(cls, number: Optional[int] = None):
        months = {
            1: "Jan",
            2: "Fev",
            3: "Mar",
            4: "Abr",
            5: "Mai",
            6: "Jun",
            7: "Jul",
            8: "Ago",
            9: "Set",
            10: "Out",
            11: "Nov",
            12: "Dez"
        }
        return months if not number else months[number]

    @classmethod
    def classify_departaments(cls, departament):
        for category, rules in categories.items():
            if departament in rules:
                return category
        return None

    @classmethod
    def filter_departament(cls, departament: str, selected: Optional[List[str]]) -> bool:
        if selected is None or not selected:
            return True
        return departament in selected

    @classmethod
    def filter_status(cls, status: str, selected: Optional[List[str]]) -> bool:
        if selected is None or not selected:
            return True
        return status in selected

    @classmethod
    def filter_date(cls, conclusion_date: date, start: Optional[date], end: Optional[date]) -> bool:
        if start and conclusion_date < start:
            return False
        if end and conclusion_date > end:
            return False
        return True

    @classmethod
    def color(cls, status:str):
        color_map = {
            "Sem Análise": "#1e7dca",
            "Resolvendo": "#f6ba2a",
            "Atrasada": "#e23512"
        }

        return color_map.get(status)

    @classmethod
    def status(cls, status):
        mapping = {
            "Responder": "Sem Análise"
        }

        return mapping.get(status, status)
