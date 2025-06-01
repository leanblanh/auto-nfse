from .entities import Cliente, Venda, NotaFiscal
from .exceptions import AddressNotFoundError, ApiPrefituraError, DDDNotFoundError, InvalidDataError
from typing import Protocol

CURSO_PARA_NOTA_MAP = {
    "Oficina Moda Fitness Modelagem e Costura de Roupas Esportivas": "Curso EAD",
    "Dayse Costa Academy MEMBROS": "Plano de Assinatura",
    "Costura Básica Para Iniciantes -Faça Suas Roupas": "Curso EAD - Costura Básica",
}

def mapear_nome_curso(nome_na_planilha:str) -> str:
    """
    Mapeia o nome do curso para o nome utilizado na nota fiscal.
    """
    return CURSO_PARA_NOTA_MAP.get(nome_na_planilha, nome_na_planilha)

class CepService(Protocol):
    def buscar_endereco(self, cep: str) -> dict:
        ...

class ApiPrefituraService(Protocol):
    def emitir_nota_fiscal(self, nota_fiscal_data: dict) -> dict:
        ...

class DDDResolverService(Protocol):
    def resolver_ddd(self, ddd: str) -> tuple[str, str]:
        ...

class NotaFiscalService:
    def __init__(
        self,
        cep_service: CepService,
        api_prefeitura_service: ApiPrefituraService,
        ddd_resolver_service: DDDResolverService
    ):
        self.cep_service = cep_service
        self.api_prefeitura_service = api_prefeitura_service
        self.ddd_resolver_service = ddd_resolver_service

    def _preencher_endereco(self, cliente: Cliente) -> Cliente:
        if cliente.cep:
            try:
                endereco = self.cep_service.buscar_endereco(cliente.cep)
                cliente.rua = endereco["logradouro"]
                cliente.bairro = endereco["bairro"]
                cliente.cidade = endereco["localidade"]
                cliente.estado = endereco["uf"]
            except AddressNotFoundError:
                print(f"Endereço não encontrado para o CEP: {cliente.cep}")
        elif cliente.telefone:
            ddd = cliente.telefone[:2]  # Pega os dois primeiros dígitos
            try:
                cidade, estado = self.ddd_resolver_service.resolver_ddd(ddd)
                cliente.cidade = cidade
                cliente.estado = estado
            except DDDNotFoundError:
                print(f"Cidade/Estado não encontrados para o DDD: {ddd}")
        else:
            raise InvalidDataError("É necessário informar CEP ou Telefone (para buscar o DDD).")
        return cliente

    def gerar_nota_fiscal(self, venda: Venda) -> NotaFiscal:
        venda.cliente = self._preencher_endereco(venda.cliente)
        nome_curso_nota = mapear_nome_curso(venda.curso)

        nota_fiscal_data = {
            "cliente": {
                "nome": venda.cliente.nome,
                "cpf": venda.cliente.cpf,
                "email": venda.cliente.email,
                "telefone": venda.cliente.telefone,
                "endereco": {
                    "rua": venda.cliente.rua,
                    "bairro": venda.cliente.bairro,
                    "cidade": venda.cliente.cidade,
                    "estado": venda.cliente.estado,
                    "numero": venda.cliente.numero,
                    "complemento": venda.cliente.complemento
                }
            },
            "itens": [{"descricao": nome_curso_nota, "valor": venda.valor}],
            "valor_total": venda.valor,
            "codigo_oferta": venda.codigo_oferta
        }

        try:
            resposta_api = self.api_prefeitura_service.emitir_nota_fiscal(nota_fiscal_data)
            numero_nota = resposta_api["numero_nota"]
            data_emissao = resposta_api["data_emissao"]
            return NotaFiscal(
                cliente=venda.cliente,
                itens=[nome_curso_nota],
                valor_total=venda.valor,
                numero=numero_nota,
                data_emissao=data_emissao
            )
        except ApiPrefituraError as e:
            print(f"Erro ao emitir nota fiscal: {e}")
            raise