from abc import ABC, abstractmethod
from datetime import date
from typing import Optional, List, Tuple


class GetTickets(ABC):

    @abstractmethod
    def get_open_tickets(self, ft_dpt:Optional[List[str]] = None, ft_stts:Optional[List[str]] = None, total: bool = False):
        pass

    @abstractmethod
    def get_by_departament(self, ft_dpt:Optional[List[str]] = None):
        pass

    @abstractmethod
    def sla_per_month(self, departament_selected: Optional[List[str]] = None, start_date: Optional[date] = None, end_date: Optional[date] = None) :
        pass

    @abstractmethod
    def get_sla(self, departament_selected: Optional[List[str]] = None, start_date: Optional[date] = None, end_date: Optional[date] = None) :
        pass

    @abstractmethod
    def get_sla_exceded(self, departament_selected: Optional[List[str]] = None, start_date: Optional[date] = None, end_date: Optional[date] = None):
        pass
