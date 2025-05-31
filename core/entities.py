# Classe de dados (Cliente, Venda, Nota Fiscal)
from dataclasses import dataclass
from typing import Optional

@dataclass
class Cliente:
    nome: str
    cpf: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    rua: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None

@dataclass
class Venda:
    cliente: Cliente
    curso: str
    valor: float
    codigo_oferta: str

@dataclass
class NotaFiscal:
    cliente: Cliente
    itens: list[str]  # Descrição dos itens da venda
    valor_total: float
    numero: str  # Número da nota fiscal gerado pela prefeitura
    data_emissao: str # Data de emissão da nota fiscal