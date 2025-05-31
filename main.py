from core.services import NotaFiscalService
from adapters.api_prefeitura import ApiPrefituraAdapter
from adapters.api_cep import ViaCepAdapter
from adapters.data_source import ExcelDataSource
from adapters.ddd_resolver import DDDResolverAdapter, DDD_DATA
from interfaces.controllers import NotaFiscalController
from config.settings import FILE_PATH

def main():
    cep_service = ViaCepAdapter()
    api_prefeitura_service = ApiPrefituraAdapter()
    ddd_resolver_service = DDDResolverAdapter(DDD_DATA)
    nota_fiscal_service = NotaFiscalService(cep_service, api_prefeitura_service, ddd_resolver_service)
    data_source = ExcelDataSource(FILE_PATH)
    controller = NotaFiscalController(nota_fiscal_service, data_source)

    controller.processar_vendas()

if __name__ == "__main__":
    main()