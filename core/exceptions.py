class DataImportError(Exception):
    """Erro ao importar dados da tabela."""
    pass

class AddressNotFoundError(Exception):
    """Endereço não encontrado."""
    pass

class ApiPrefituraError(Exception):
    """Erro na comunicação com a API da prefeitura."""
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code

class DDDNotFoundError(Exception):
    """DDD não encontrado."""
    pass

class InvalidDataError(Exception):
    """Dados inválidos."""
    pass