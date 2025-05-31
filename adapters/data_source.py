import pandas as pd
from core.entities import Cliente, Venda
from core.exceptions import DataImportError
import openpyxl

class CSVDataSource:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def ler_dados(self) -> list[Venda]:
        try:
            df = pd.read_csv(self.file_path)
            vendas = []
            for _, row in df.iterrows():
                cliente = Cliente(
                    nome=row["nome"],
                    cpf=row.get("cpf"),
                    email=row.get("email"),
                    telefone=row.get("telefone"),
                    rua=row.get("rua"),
                    bairro=row.get("bairro"),
                    cidade=row.get("cidade"),
                    estado=row.get("estado"),
                    numero=row.get("numero"),
                    complemento=row.get("complemento"),
                    cep=row.get("cep")
                )
                venda = Venda(
                    cliente=cliente,
                    curso=row["curso"],
                    valor=row["valor"],
                    codigo_oferta=row["codigo_oferta"]
                )
                vendas.append(venda)
            return vendas
        except FileNotFoundError:
            raise DataImportError(f"Arquivo não encontrado: {self.file_path}")
        except pd.errors.EmptyDataError:
            raise DataImportError(f"Arquivo vazio: {self.file_path}")
        except pd.errors.ParserError:
            raise DataImportError(f"Erro ao analisar o arquivo: {self.file_path}")

class ExcelDataSource:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def ler_dados(self) -> list[Venda]:
        try:
            workbook = openpyxl.load_workbook(self.file_path)
            sheet = workbook.active  # Ou especifique a planilha: workbook["NomeDaPlanilha"]
            vendas = []
            # Assumimos que a primeira linha contém os cabeçalhos
            header = [cell.value for cell in sheet[1]]
            # Encontra os índices das colunas (case-insensitive)
            def get_column_index(header, column_name):
                try:
                    return header.index(column_name)
                except ValueError:
                    try:
                        return header.index(column_name.lower())
                    except ValueError:
                        raise DataImportError(f"Coluna '{column_name}' não encontrada no arquivo Excel.")

            nome_index = get_column_index(header, "nome")
            cpf_index = get_column_index(header, "cpf")
            email_index = get_column_index(header, "email")
            telefone_index = get_column_index(header, "telefone")
            rua_index = get_column_index(header, "rua")
            bairro_index = get_column_index(header, "bairro")
            cidade_index = get_column_index(header, "cidade")
            estado_index = get_column_index(header, "estado")
            numero_index = get_column_index(header, "numero")
            complemento_index = get_column_index(header, "complemento")
            curso_index = get_column_index(header, "curso")
            valor_index = get_column_index(header, "valor")
            codigo_oferta_index = get_column_index(header, "codigo_oferta")

            for row in sheet.iter_rows(min_row=2, values_only=True):  # Ignora a primeira linha (cabeçalho)
                cliente = Cliente(
                    nome=row[nome_index],
                    cpf=row[cpf_index] if cpf_index is not None and row[cpf_index] is not None else None,
                    email=row[email_index] if email_index is not None and row[email_index] is not None else None,
                    telefone=row[telefone_index] if telefone_index is not None and row[telefone_index] is not None else None,
                    rua=row[rua_index] if rua_index is not None and row[rua_index] is not None else None,
                    bairro=row[bairro_index] if bairro_index is not None and row[bairro_index] is not None else None,
                    cidade=row[cidade_index] if cidade_index is not None and row[cidade_index] is not None else None,
                    estado=row[estado_index] if estado_index is not None and row[estado_index] is not None else None,
                    numero=row[numero_index] if numero_index is not None and row[numero_index] is not None else None,
                    complemento=row[complemento_index] if complemento_index is not None and row[complemento_index] is not None else None,
                )
                venda = Venda(
                    cliente=cliente,
                    curso=row[curso_index],
                    valor=row[valor_index],
                    codigo_oferta=row[codigo_oferta_index]
                )
                vendas.append(venda)
            return vendas
        except FileNotFoundError:
            raise DataImportError(f"Arquivo não encontrado: {self.file_path}")
        except openpyxl.utils.exceptions.InvalidFileException:
            raise DataImportError(f"Arquivo inválido (não é um arquivo Excel válido): {self.file_path}")
        except Exception as e:
            raise DataImportError(f"Erro ao ler o arquivo: {e}")