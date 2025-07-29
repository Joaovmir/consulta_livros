# models/health.py
from pydantic import BaseModel
from typing import List

class HealthCheckResponse(BaseModel):
    """Modelo de resposta para a verificação de saúde da API."""
    status: str
    mensagem: str
    livros_carregados: int
    categorias_disponiveis: List[str]
    quantidade_categorias: int
    verificado_em: str
    tempo_resposta_ms: float