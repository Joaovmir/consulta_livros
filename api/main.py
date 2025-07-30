# main.py
import pandas as pd
import time
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, Query, HTTPException, status, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# JWT Authentication
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api.auth import authenticate_user, create_access_token, get_current_user
from models.user import User
from api.auth import get_db
from datetime import timedelta

# scripts/webscraping_livros.py função rodar_scraping
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # permite importar de /scripts

from scripts.webscraping_livros import rodar_scraping

# ---------------------------------------------------------------------------
# 1. Definição dos Modelos de Dados com Pydantic
# ---------------------------------------------------------------------------

from models.book_models import Book, StatsOverview, CategoryStats
from models.health import HealthCheckResponse
from models.user import User

# ---------------------------------------------------------------------------
# 2. Inicialização do FastAPI e Carregamento dos Dados
# ---------------------------------------------------------------------------

app = FastAPI(
    title="API de Livros",
    description="Uma API para consultar informações sobre livros de uma livraria fictícia.",
    version="1.0.0",
    contact={
        "name": "Seu Nome",
        "url": "http://seusite.com",
        "email": "seu@email.com",
    },
)

# --- Carregamento e Preparação dos Dados ---

try:
    # O caminho para o CSV deve ser relativo ao local onde você executa o uvicorn
    dados_livros = pd.read_csv("../data/info_livros.csv", sep=";")
    
    # Adiciona uma coluna 'id' baseada no índice do DataFrame
    dados_livros.reset_index(inplace=True)
    dados_livros.rename(columns={'index': 'id'}, inplace=True)
    
    # Conversão de tipos para garantir consistência
    dados_livros['preco'] = pd.to_numeric(dados_livros['preco'], errors='coerce').fillna(0)
    dados_livros['avaliacao'] = pd.to_numeric(dados_livros['avaliacao'], errors='coerce').fillna(0)
    dados_livros['estoque'] = pd.to_numeric(dados_livros['estoque'], errors='coerce').fillna(0).astype(int)
    dados_livros['disponibilidade'] = dados_livros['disponibilidade'].astype(bool)

except FileNotFoundError:
    print("ERRO: O arquivo 'info_livros.csv' não foi encontrado. Certifique-se de que ele está na mesma pasta que o 'main.py'.")
    # Cria um DataFrame vazio para evitar que a API quebre ao iniciar
    dados_livros = pd.DataFrame(columns=['id', 'titulo', 'preco', 'avaliacao', 'disponibilidade', 'estoque', 'categoria', 'imagem'])


# ---------------------------------------------------------------------------
# 3. Endpoints da API
# ---------------------------------------------------------------------------

@app.get(
    "/api/v1/health",
    response_model=HealthCheckResponse,
    summary="Verifica a saúde da API",
    tags=["Status"]
)
def health_check():
    """
    Fornece um status detalhado da API, incluindo o número de livros carregados,
    categorias disponíveis e tempo de resposta.
    """
    try:
        start = time.time()
        num_livros = len(dados_livros)
        categorias = sorted(dados_livros["categoria"].dropna().unique().tolist())
        duracao = round((time.time() - start) * 1000, 2)

        content = {
            "status": "OK",
            "mensagem": "API de Livros está funcionando perfeitamente 🚀",
            "livros_carregados": num_livros,
            "categorias_disponiveis": categorias,
            "quantidade_categorias": len(categorias),
            "verificado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "tempo_resposta_ms": duracao
        }
        return JSONResponse(status_code=status.HTTP_200_OK, content=content)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"mensagem": "Erro ao verificar a saúde da API 😞", "erro": str(e)}
        )

@app.get(
    "/api/v1/books",
    response_model=List[Book],
    summary="Obter todos os livros",
    description="Retorna uma lista de todos os livros disponíveis na base de dados.",
    tags=["Livros"]
)
def get_livros():
    """Endpoint para obter a lista completa de livros."""
    if dados_livros.empty:
        return []
    return dados_livros.to_dict(orient="records")

@app.get(
    "/api/v1/books/{id_livro}",
    response_model=Book,
    summary="Obter um livro por ID",
    tags=["Livros"]
)
def get_livro_id(id_livro: int = Path(..., description="O ID do livro a ser buscado.", gt=-1)):
    """
    Busca um livro específico pelo seu ID. Retorna 404 se o livro não for encontrado.
    """
    livro = dados_livros[dados_livros['id'] == id_livro]
    if livro.empty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Livro com ID {id_livro} não encontrado.")
    # .to_dict() retorna uma lista, pegamos o primeiro (e único) item
    return livro.to_dict(orient="records")[0]

@app.get(
    "/api/v1/books/search",
    response_model=List[Book],
    summary="Buscar livros por título e/ou categoria",
    tags=["Livros"]
)
def search_livros(
    title: Optional[str] = Query(None, description="Parte do título do livro para buscar."),
    category: Optional[str] = Query(None, description="Categoria do livro para filtrar.")
):
    """
    Permite a busca de livros filtrando por título e/ou categoria.
    A busca não diferencia maiúsculas de minúsculas.
    """
    resultado = dados_livros
    if title:
        resultado = resultado[resultado["titulo"].str.contains(title, case=False, na=False)]
    if category:
        resultado = resultado[resultado["categoria"].str.contains(category, case=False, na=False)]
    
    return resultado.to_dict(orient="records")

@app.get(
    "/api/v1/books/top-rated",
    response_model=List[Book],
    summary="Obter livros com melhor avaliação",
    tags=["Livros"]
)
def livros_top_avaliados(quantidade: int = Query(10, description="Número de livros a retornar.", gt=0, le=100)):
    """Retorna os livros com as maiores notas de avaliação, em ordem decrescente."""
    top = dados_livros.sort_values(by="avaliacao", ascending=False).head(quantidade)
    return top.to_dict(orient="records")

@app.get(
    "/api/v1/books/price-range",
    response_model=List[Book],
    summary="Filtrar livros por faixa de preço",
    tags=["Livros"]
)
def livros_por_preco(
    min_price: float = Query(0.0, description="Preço mínimo.", ge=0),
    max_price: float = Query(10000.0, description="Preço máximo.", ge=0)
):
    """Busca livros que estão dentro de uma faixa de preço específica (inclusivo)."""
    filtrado = dados_livros[
        (dados_livros["preco"] >= min_price) & (dados_livros["preco"] <= max_price)
    ]
    return filtrado.to_dict(orient="records")

@app.get(
    "/api/v1/categories",
    response_model=List[str],
    summary="Listar todas as categorias",
    tags=["Categorias"]
)
def get_categorias():
    """Retorna uma lista ordenada com todas as categorias de livros únicas."""
    categorias = dados_livros["categoria"].dropna().unique().tolist()
    return sorted(categorias)

@app.get(
    "/api/v1/stats/overview",
    response_model=StatsOverview,
    summary="Obter estatísticas gerais",
    tags=["Estatísticas"]
)
def stats_overview():
    """Fornece um resumo estatístico de todo o acervo de livros."""
    if dados_livros.empty:
        return {"total_livros": 0, "preco_medio": 0, "avaliacao_media": 0, "estoque_total": 0}
        
    total_livros = len(dados_livros)
    preco_medio = round(dados_livros["preco"].mean(), 2)
    avaliacao_media = round(dados_livros["avaliacao"].mean(), 2)
    total_estoque = int(dados_livros["estoque"].sum())

    return {
        "total_livros": total_livros,
        "preco_medio": preco_medio,
        "avaliacao_media": avaliacao_media,
        "estoque_total": total_estoque
    }

@app.get(
    "/api/v1/stats/categories",
    response_model=List[CategoryStats],
    summary="Obter estatísticas por categoria",
    tags=["Estatísticas"]
)
def stats_por_categoria():
    """Agrupa os livros por categoria e calcula estatísticas para cada uma."""
    if dados_livros.empty or 'categoria' not in dados_livros.columns:
        return []
        
    stats = dados_livros.groupby("categoria").agg(
        total_livros=("titulo", "count"),
        preco_medio=("preco", "mean"),
        avaliacao_media=("avaliacao", "mean"),
        estoque_total=("estoque", "sum")
    ).reset_index()

    stats["preco_medio"] = stats["preco_medio"].round(2)
    stats["avaliacao_media"] = stats["avaliacao_media"].round(2)
    stats["estoque_total"] = stats["estoque_total"].astype(int)

    return stats.to_dict(orient="records")

# EP login
@app.post("/api/v1/auth/login", tags=["Autenticação"])
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Realiza login e retorna um token JWT se as credenciais estiverem corretas.
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    
    token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}

# EP refresh
@app.post("/api/v1/auth/refresh", tags=["Autenticação"])
def refresh_token(current_user: User = Depends(get_current_user)):
    """
    Gera um novo token JWT para o usuário logado.
    """
    new_token = create_access_token(data={"sub": current_user.username})
    return {"access_token": new_token, "token_type": "bearer"}

# EP scraping
@app.post("/api/v1/scraping/trigger", tags=["Admin"])
def executar_scraping(current_user: User = Depends(get_current_user)):
    """
    Executa o scraping de livros. Disponível apenas para usuários administradores.
    """
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Acesso negado: você não é admin.")
    
    try:
        rodar_scraping()
        return {"mensagem": "Scraping executado com sucesso e dados atualizados!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao executar o scraping: {str(e)}")

    # # REMOVER O return PARA ADICIONAR O SCRIPT DE SCRAPING ACIMA
    # return {"mensagem": "Scraping iniciado com sucesso! 🚀"}
