import re
from core.exceptions import InvalidDataError

def validar_cpf(cpf: str) -> None:
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        raise InvalidDataError("CPF inválido.")
    # Implemente a lógica de validação do CPF aqui (opcional, mas recomendado)

def validar_email(email: str) -> None:
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise InvalidDataError("Email inválido.")