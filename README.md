# Projeto: API de Consulta de Livros

Este projeto consiste em duas partes principais que trabalham em conjunto:

1.  **Web Scraper**: Um script em Python (`scripts/webscraping_livros.py`) que utiliza Selenium para extrair dados de livros do site [Books to Scrape](http://books.toscrape.com). Os dados recolhidos são guardados num ficheiro CSV.
2.  **API REST**: Uma API (`api/main.py`) construída com FastAPI que lê o ficheiro CSV e disponibiliza os dados através de vários endpoints, permitindo consultas, filtros e a visualização de estatísticas.

-----

## 📂 Estrutura de Pastas

O projeto está organizado da seguinte forma para manter o código limpo e modular:

```
/CONSULTA_LIVROS/
│
├── api/
│   ├── main.py              # Código principal da API FastAPI
│   ├── auth.py              # Lógica de autenticação com JWT
│
├── database/
│   ├── db.py                # Conexão com SQLite usando SQLAlchemy
│   ├── init_db.py           # Criação da tabela users e usuário admin
│   └── users.db             # Arquivo do banco de dados SQLite
│
├── models/
│   ├── user.py              # Modelo SQLAlchemy para User
│   ├── book_models.py       # Modelos Pydantic para livros e estatísticas
│   └── health.py            # Modelo Pydantic para o health check
│
├── scripts/
│   └── webscraping_livros.py  # Script de scraping de livros
│
├── data/
│   └── info_livros.csv      # Arquivo CSV com os dados extraídos do site
│
├── requirements.txt         # Lista de dependências do projeto
├── README.md                # Documentação do projeto
└── .gitignore               # Arquivos/pastas ignoradas pelo Git
|
... (outros ficheiros de configuração)
```

-----

## ⚙️ Pré-requisitos

Antes de começar, certifique-se de que tem o **Python 3.10+** instalado. Depois, abra o seu terminal na pasta raiz do projeto (`/CONSULTA_LIVROS/`) e instale todas as bibliotecas necessárias a partir do ficheiro `requirements.txt`.

```bash
pip install -r requirements.txt
```

-----

## 🚀 Como Executar o Projeto

Siga estes passos na ordem correta. **Execute todos os comandos a partir da pasta raiz do projeto (`/CONSULTA_LIVROS/`)**.

### **(Opcional) Passo 1: Extrair os Dados**

Caso ainda não tenha o arquivo de dados, execute o scraping. O scraping só pode ser executado via endpoint da API, pois implementamos autenticação para proteger a rota, e requer um **usuário autenticado com perfil admin**.

1. Inicie a API:
```bash
uvicorn api.main:app --reload
```

2. Faça login (via Postman):
- Método: POST
- URL: http://127.0.0.1:8000/api/v1/auth/login
- Body (x-www-form-urlencoded):
  - username: admin
  - password: admin123

Copie o access_token da resposta.

3. Faça a chamada para o endpoint de scraping:
- Método: POST
- URL: http://127.0.0.1:8000/api/v1/scraping/trigger
  - Headers:
    - Authorization: Bearer <cole_seu_token_aqui>

Isso irá:

1.  Solicitar no terminal se "Deseja abrir o navegador visivelmente? (s/n)"
2.  Iniciar um navegador Chrome em segundo plano (modo *headless*).
3.  Navegar pelo site `books.toscrape.com` e recolher os dados.
4.  Criar a pasta `data/` (se não existir) 
5.  Solicitar "Escreva um nome para o arquivo de dados (apenas o nome, sem o formato .csv):"
6.  Informe o nome `info_livros`.
7.  Guardar tudo no ficheiro `data/info_livros.csv`.

Aguarde até que a mensagem `✅ Arquivo salvo com sucesso.` apareça no terminal.

### **Passo 2: Iniciar a API**

Caso não tenha iniciado a API mas já tem o ficheiro `info_livros.csv` já criado, pode iniciar o servidor da API.

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
