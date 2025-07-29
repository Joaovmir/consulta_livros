# models/book_models.py
from pydantic import BaseModel, Field
from typing import List

class Book(BaseModel):
    """Modelo de dados para um livro."""
    id: int = Field(..., description="ID único do livro.")
    titulo: str = Field(..., description="Título do livro.")
    preco: float = Field(..., description="Preço do livro.")
    avaliacao: float = Field(..., description="Avaliação média do livro (0 a 5).")
    disponibilidade: bool = Field(..., description="Indica se o livro está disponível.")
    estoque: int = Field(..., description="Quantidade em estoque.")
    categoria: str = Field(..., description="Categoria do livro.")
    imagem: str = Field(..., description="URL da imagem de capa do livro.")

    class Config:
        from_attributes = True

class StatsOverview(BaseModel):
    """Modelo de resposta para as estatísticas gerais."""
    total_livros: int
    preco_medio: float
    avaliacao_media: float
    estoque_total: int

class CategoryStats(BaseModel):
    """Modelo de resposta para as estatísticas por categoria."""
    categoria: str
    total_livros: int
    preco_medio: float
    avaliacao_media: float
    estoque_total: int