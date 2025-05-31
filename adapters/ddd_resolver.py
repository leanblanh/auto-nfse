from core.exceptions import DDDNotFoundError

class DDDResolverAdapter:
    def __init__(self, ddd_data: dict[str, tuple[str, str]]):
        self.ddd_data = ddd_data

    def resolver_ddd(self, ddd: str) -> tuple[str, str]:
        if ddd in self.ddd_data:
            return self.ddd_data[ddd]
        else:
            raise DDDNotFoundError(f"DDD {ddd} não encontrado.")

# Exemplo de dados (pode vir de um arquivo ou banco de dados)
DDD_DATA = {
    "21": ("Rio de Janeiro", "RJ"),
    "11": ("São Paulo", "SP"),
    # ... complete com mais DDDs
}

ddd_resolver = DDDResolverAdapter(DDD_DATA)