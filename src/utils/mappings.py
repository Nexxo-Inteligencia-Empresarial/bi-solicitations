from typing import Optional, List
from .map_departaments import departaments

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
    def classify_departaments(cls, departament:str):
        departament = departament.title()
        dpt = departaments.get(departament)

        if departament: return departament
        if departament == "Departamento Pessoal": return "Folha"

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

    @classmethod
    def ticket_to_dict(cls, ticket):
        return {
            "Ticket": ticket.ticket_id,
            "Departamento": ticket.departament,
            "Responsável": ticket.responsible,
            "Criado em": ticket.create_date,
            "Concluído em": ticket.conclusion_date,
            "Sistema": ticket.system,
            "Tipo": ticket.type,
            "Reaberta": ticket.reopen
        }

    @classmethod
    def categories(cls):
        return [
                "Alteração de CBO/Função",
                "Alteração de contrato de trabalho",
                "Analisar Termo de Intimação",
                "Análise Termo de Notificação",
                "Dúvidas Gerais",
                "Enviar Chave do FGTS",
                "Extrato Analítico",
                "Lançamento de Atestado",
                "Lançamento de Falta",
                "Lançamento de Pensão Alimentícia",
                "Projeção de Custo",
                "Simulação de Férias",
                "Simulação de Rescisão",
                "Solicitar PERDCOMP(GERAL)",
                "Cálculo de Férias(GERAL)",
                "Cálculo de Rescisão",
                "Transferência de Empregados(GERAL)",
                "Alteração de data Aviso Prévio",
                "Aviso de Férias",
                "Aviso de Rescisão",
                "Envio de Contracheque",
                "Envio de Ficha de Registro",
                "Exclusão de Admissão",
                "Levantamento de FGTS",
                "Análise de Escala de Trabalho",
                "Lançamento de Rubricas",
                "Admissão",
                "Afastamento"
            ]
