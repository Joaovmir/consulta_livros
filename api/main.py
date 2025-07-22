from fastapi import FastAPI, status, HTTPException, Query
from fastapi.responses import JSONResponse
from datetime import datetime
import time
from typing import Optional
import pandas as pd

app = FastAPI(title="API de Livros")

dados_livros = pd.read_csv("../data/info_livros.csv", sep=";")

def tabela_para_json(linha):
    return {
        "id": linha.name,
        "titulo": linha["titulo"],
        "preco": linha["preco"],
        "avaliacao": linha["avaliacao"],
        "disponibilidade": linha["disponibilidade"],
        "estoque": linha["estoque"],
        "categoria": linha["categoria"],
        "imagem": linha["imagem"],
    }

@app.get("/api/v1/health")
def health_check():
    try:
        start = time.time()

        num_livros = len(dados_livros)
        categorias = sorted(dados_livros["categoria"].dropna().unique().tolist())
        duracao = round((time.time() - start) * 1000, 2)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "OK",
                "mensagem": "API de Livros está funcionando perfeitamente 🚀",
                "livros_carregados": num_livros,
                "categorias_disponiveis": categorias,
                "quantidade_categorias": len(categorias),
                "verificado_em": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "tempo_resposta_ms": duracao
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": "erro",
                "mensagem": "Erro ao verificar a saúde da API 😞",
                "detalhes": str(e)
            }
        )

@app.get("/api/v1/books")
def get_livros():
    return [tabela_para_json(linha) for _, linha in dados_livros.iterrows()]

@app.get("/api/v1/book/{id_livro}")
def get_livro_id(id_livro: int):
    if 0 <= id_livro < len(dados_livros):
        return [tabela_para_json(linha) for _, linha in dados_livros.iloc[[id_livro]].iterrows()]
    raise HTTPException(status_code=404, detail="Livro não encontrado")


@app.get("/api/v1/books/search")
def search_livros(title: Optional[str] = Query(None), category: Optional[str] = Query(None)):
    resultado = dados_livros
    if title:
        resultado = resultado[resultado["titulo"].str.contains(title, case=False, na=False)]
    if category:
        resultado = resultado[resultado["categoria"].str.contains(category, case=False, na=False)]
    return [tabela_para_json(linha) for _, linha in resultado.iterrows()]

@app.get("/api/v1/categories")
def get_categorias():
    categorias = dados_livros["categoria"].dropna().unique().tolist()
    return sorted(categorias)

