from typing import Optional

class MapMonths:
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
