import requests
from core.exceptions import AddressNotFoundError

class ViaCepAdapter:
    def buscar_endereco(self, cep: str) -> dict:
        try:
            response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
            response.raise_for_status()
            data = response.json()
            if "erro" in data:
                raise AddressNotFoundError(f"CEP {cep} não encontrado.")
            return data
        except requests.exceptions.RequestException as e:
            raise AddressNotFoundError(f"Erro ao buscar CEP: {e}")