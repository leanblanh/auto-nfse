import requests
from core.exceptions import ApiPrefituraError
from config.settings import API_PREFEITURA_URL, API_PREFEITURA_TOKEN

class ApiPrefituraAdapter:
    def __init__(self, url: str = API_PREFEITURA_URL, token: str = API_PREFEITURA_TOKEN):
        self.url = url
        self.token = token

    def emitir_nota_fiscal(self, nota_fiscal_data: dict) -> dict:
        headers = {"Authorization": f"Bearer {self.token}"}  # Ajuste conforme a autenticação da API
        response = None
        try:
            response = requests.post(f"{self.url}/notas", json=nota_fiscal_data, headers=headers)
            response.raise_for_status()  # Lança exceção para status HTTP de erro
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ApiPrefituraError(str(e), response.status_code if response else 500)