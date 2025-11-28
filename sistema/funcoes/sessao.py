
import os


BASE_URL = os.getenv("API_URL", "http://localhost:3000")

# Variáveis globais de estado
token = None
usuario_id = None
usuario_nome = None

def get_headers():
    """
    Retorna o cabeçalho de autorização padrão para as requisições.  Se não houver token, retorna um dicionário vazio (ou lança erro).
    """
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}