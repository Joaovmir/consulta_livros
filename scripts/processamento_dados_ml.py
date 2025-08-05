# scripts/processamento_dados_ml.py
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def carregar_dados(nome_arquivo:str = 'info_livros.csv'):
    """Lê os dados do arquivo CSV do scraping."""

    return pd.read_csv(f'data/{nome_arquivo}', sep=';') # Contando que sempre será salvo na pasta data

def ml_features():
    """
    Retorna um DataFrame pronto para ser usado como input de modelos ML.
    Inclui: preco, avaliacao, estoque, disponibilidade (binária), categoria (codificada) e id do livro.
    """
    df = carregar_dados()
    
    # Propostas de formatação de features para o projeto de recomendação de livros:
    # 1 - Garantir colunas numéricas
    # 2 - Mapear disponibilidade: "In stock" = 1, caso contrário = 0
    # 3 - Codificar categoria
    # 4 - Selecionar as colunas de features // todas menos as imagens

    # 1. 
    df['preco'] = pd.to_numeric(df['preco'], errors="coerce").fillna(0)
    df['avaliacao'] = pd.to_numeric(df['avaliacao'], errors="coerce").fillna(0)
    df['estoque'] = pd.to_numeric(df['estoque'], errors="coerce").fillna(0).astype(int)

    # 2. 
    df['disponibilidade'] = df['disponibilidade'].apply(lambda x: 1 if str(x).strip().lower() == "in stock" else 0)

    # 3. 
    le = LabelEncoder()
    df['categoria_codificada'] = le.fit_transform(df['categoria'].astype(str))

    # 4. 
    colunas_final = ["titulo", "preco", "avaliacao", "estoque", "disponibilidade", "categoria_codificada"]
    return df[colunas_final]


def ml_training_data():
    """
    Retorna 80% dos dados (amostragem aleatória) para treinamento de modelos.
    Inclui todas as colunas de features.
    """
    df = ml_features()

    df_treino, _ = train_test_split(df, test_size=0.2, random_state=40)

    return df_treino