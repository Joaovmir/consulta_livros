# Projeto: API de Consulta de Livros

Este projeto consiste em duas partes principais que trabalham em conjunto:

1.  **Web Scraper**: Um script em Python (`scripts/webscraping_livros.py`) que utiliza Selenium para extrair dados de livros do site [Books to Scrape](http://books.toscrape.com). Os dados recolhidos são guardados num ficheiro CSV.
2.  **API REST**: Uma API (`api/main.py`) construída com FastAPI que lê o ficheiro CSV e disponibiliza os dados através de vários endpoints, permitindo consultas, filtros e a visualização de estatísticas.

-----

## 📂 Estrutura de Pastas

O projeto está organizado da seguinte forma para manter o código limpo e modular:

```
/CONSULTA_LIVROS/
|
|-- api/
|   |-- main.py            # O código da API FastAPI
|
|-- data/
|   |-- info_livros.csv    # Ficheiro de dados gerado pelo scraper
|
|-- scripts/
|   |-- webscraping_livros.py # O script para extrair os dados
|
|-- .gitignore             # Ficheiros e pastas a serem ignorados pelo Git
|-- README.md              # Este ficheiro de documentação
|-- requirements.txt       # Lista de dependências Python
|
... (outros ficheiros de configuração)
```

-----

## ⚙️ Pré-requisitos

Antes de começar, certifique-se de que tem o **Python** instalado. Depois, abra o seu terminal na pasta raiz do projeto (`/CONSULTA_LIVROS/`) e instale todas as bibliotecas necessárias a partir do ficheiro `requirements.txt`.

```bash
# Instala todas as dependências de uma só vez
pip install -r requirements.txt
```

-----

## 🚀 Como Executar o Projeto

Siga estes passos na ordem correta. **Execute todos os comandos a partir da pasta raiz do projeto (`/CONSULTA_LIVROS/`)**.

### **Passo 1: Extrair os Dados (Executar o Scraper)**

Primeiro, precisamos de criar o nosso ficheiro de dados. Para isso, execute o script de scraping.

```bash
python scripts/webscraping_livros.py
```

O script irá:

1.  Iniciar um navegador Chrome em segundo plano (modo *headless*).
2.  Navegar pelo site `books.toscrape.com` e recolher os dados.
3.  Criar a pasta `data/` (se não existir) e guardar tudo no ficheiro `data/info_livros.csv`.

Aguarde até que a mensagem `✅ Arquivo salvo com sucesso.` apareça no terminal.

### **Passo 2: Iniciar a API**

Com o ficheiro `info_livros.csv` já criado, pode iniciar o servidor da API.

```bash
uvicorn api.main:app --reload
```

  * `api.main`: Indica ao Uvicorn para procurar o objeto `app` dentro do ficheiro `main.py` que está na pasta `api/`.
  * `--reload`: Reinicia o servidor automaticamente sempre que fizer alterações no código.

O terminal deverá mostrar uma mensagem a indicar que o servidor está a funcionar:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### **Passo 3: Ver a Documentação e Usar a API**

Agora que o servidor está ativo, abra o seu navegador de internet e aceda ao seguinte endereço:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Irá ver a documentação interativa do **Swagger UI**, onde pode explorar e testar todos os endpoints da sua API diretamente no navegador.