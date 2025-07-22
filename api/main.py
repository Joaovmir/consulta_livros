from fastapi import FastAPI, HTTPException, Query
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
    return {"status": "ok"}

@app.get("/api/v1/books")
def get_livros():
    return [tabela_para_json(linha) for _, linha in dados_livros.iterrows()]

@app.get("/api/v1/book/{id_livro}")
def get_livro_id(id_livro: int):
    if 0 <= id_livro < len(dados_livros):
        return [tabela_para_json(linha) for _, linha in dados_livros.iloc[[int(id_livro)]].iterrows()]
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

