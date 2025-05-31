from core.services import NotaFiscalService
from adapters.data_source import ExcelDataSource
from core.exceptions import DataImportError, ApiPrefituraError

class NotaFiscalController:
    def __init__(self, nota_fiscal_service: NotaFiscalService, data_source: ExcelDataSource):
        self.nota_fiscal_service = nota_fiscal_service
        self.data_source = data_source

    def processar_vendas(self):
        try:
            vendas = self.data_source.ler_dados()
            for venda in vendas:
                try:
                    nota_fiscal = self.nota_fiscal_service.gerar_nota_fiscal(venda)
                    print(f"Nota Fiscal emitida: {nota_fiscal.numero} para {nota_fiscal.cliente.nome}")
                except ApiPrefituraError as e:
                    print(f"Erro ao processar venda para {venda.cliente.nome}: {e}")
        except DataImportError as e:
            print(f"Erro ao ler dados: {e}")