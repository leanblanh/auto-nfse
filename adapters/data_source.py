import pandas as pd
from core.entities import Cliente, Venda
from core.exceptions import DataImportError

class ExcelDataSource:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def ler_dados(self) -> list[Venda]:
        try:
            df = pd.read_excel(self.file_path)
            vendas = []
            for _, row in df.iterrows():
                try:  # Tratamento de erro individual por linha
                    cliente = Cliente(
                        nome=str(row.get("Nome", "")).strip(),  # Valor padrão e remove espaços
                        cpf=row.get("Documento", ""),
                        email=row.get("Email", ""),
                        ddd=row.get("DDD", ""),  # Mantido, mas não usado diretamente em Cliente
                        telefone=row.get("Telefone", ""),
                        cep=row.get("CEP", ""),
                        rua=str(row.get("Endereço", "")).strip(),
                        bairro=str(row.get("Bairro", "")).strip(),
                        cidade=str(row.get("Cidade", "")).strip(),
                        estado=row.get("Estado", ""),
                        numero=str(row.get("Número", "")).strip(),
                        complemento=str(row.get("Complemento", "")).strip(),
                    )
                    # Tratamento para Preço do Produto
                    preco_str = str(row.get("Preço do Produto", "0")).replace(",", ".")
                    valor = float(preco_str) if preco_str else 0.0

                    venda = Venda(
                        cliente=cliente,
                        curso=str(row.get("Nome do Produto", "")).strip(),
                        valor=valor,
                        codigo_oferta=str(row.get("Código de Oferta", "")).strip()
                    )
                    vendas.append(venda)
                except Exception as e:
                    print(f"Erro ao processar linha: {row.to_dict()}. Erro: {e}")  # Log detalhado
                    # Decida se quer continuar ou interromper aqui
                    continue  # Pula para a próxima linha
                    # raise  # Se quiser interromper a leitura na primeira falha

            return vendas
        except FileNotFoundError:
            raise DataImportError(f"Arquivo não encontrado: {self.file_path}")
        except ValueError:
            raise DataImportError(f"Erro ao ler o arquivo Excel. Verifique se o formato é válido.")
        except Exception as e:
            raise DataImportError(f"Erro inesperado ao ler o arquivo: {e}")