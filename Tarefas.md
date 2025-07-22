Claro, aqui está a lista de tarefas formatada para um arquivo Markdown, sem as citações.

### Entregáveis Obrigatórios

Aqui está a lista dos itens que você deve obrigatoriamente entregar.

**1. Repositório no GitHub Organizado**
* **Estrutura do Código:** O código deve ser organizado em módulos distintos (ex: `scripts/`, `api/`, `data/`).
* **README Completo:** O arquivo `README.md` precisa conter:
    * Descrição do projeto e da arquitetura implementada.
    * Instruções claras para instalação e configuração do ambiente.
    * Documentação detalhada de todas as rotas da API.
    * Exemplos de requisições e respostas para cada endpoint (requests/responses).
    * Instruções sobre como executar o projeto.

**2. Sistema de Web Scraping**
* **Script de Extração:** Desenvolver um script automatizado para coletar dados do site `https://books.toscrape.com/`.
* **Armazenamento Local:** Os dados extraídos devem ser salvos localmente em um arquivo no formato CSV.
* **Documentação:** O script precisa ser bem documentado e ser facilmente executável.

**3. API RESTful Funcional**
* **Tecnologia:** A API deve ser desenvolvida utilizando Flask ou FastAPI.
* **Endpoints:** É necessário implementar todos os endpoints obrigatórios listados no documento.
* **Documentação da API:** A API deve ser documentada utilizando Swagger (ou similar).

**4. Deploy Público**
* **Plataforma:** A API precisa ser publicada em uma plataforma como Heroku, Render, Vercel, ou Fly.io.
* **Acessibilidade:** Você deve fornecer um link público e funcional para a API.
* **Operacionalidade:** A API deve estar totalmente funcional no ambiente de produção.

**5. Plano Arquitetural**
* **Documentação:** Criar um diagrama ou um documento que detalhe:
    * O pipeline de dados completo: da ingestão e processamento até a API e o consumo.
    * Uma arquitetura projetada para ser escalável no futuro.
    * Um plano para integração com modelos de Machine Learning.
    * Um cenário de uso da API por cientistas de dados.

**6. Vídeo de Apresentação**
* **Duração:** O vídeo deve ter entre 3 e 12 minutos.
* **Conteúdo:**
    * Demonstração técnica geral do projeto.
    * Apresentação da arquitetura e do pipeline de dados.
    * Execução de chamadas reais à API em produção.
    * Comentários sobre as boas práticas de desenvolvimento que foram implementadas.

**7. Curso Google Cloud Generative AI**
* **Atividade Obrigatória:** Realizar os cursos da Google Cloud: "Beginner: Introduction to Generative AI Learning Path" e "Advanced: Generative AI for Developers Learning Path".
* **Comprovação:** Enviar o comprovante de conclusão dos cursos junto aos outros entregáveis para garantir 10 pontos na nota final do Tech Challenge.

---

### Objetivos Técnicos e Endpoints da API

Estes são os requisitos técnicos específicos para o web scraping e para a API.

**Web Scraping Robusto**
* **Extração Completa:** Extrair todos os livros disponíveis no site.
* **Campos de Dados:** Capturar as seguintes informações para cada livro: título, preço, `rating` (avaliação), disponibilidade, categoria e imagem.

**Endpoints Obrigatórios da API**
* `GET /api/v1/health`: Verifica o status da API.
* `GET /api/v1/books`: Lista todos os livros disponíveis.
* `GET /api/v1/books/{id}`: Retorna os detalhes de um livro específico.
* `GET /api/v1/books/search?title={title}&category={category}`: Permite a busca de livros por título e/ou categoria.
* `GET /api/v1/categories`: Lista todas as categorias de livros existentes.

---

### Desafios Adicionais (Bônus)

Estas são tarefas opcionais que você pode implementar para aprimorar seu projeto.

**Endpoints de Insights (Opcionais)**
* `GET /api/v1/stats/overview`: Fornece estatísticas gerais da coleção (total de livros, preço médio, etc.).
* `GET /api/v1/stats/categories`: Apresenta estatísticas por categoria (quantidade de livros, preços, etc.).
* `GET /api/v1/books/top-rated`: Lista os livros com a avaliação mais alta.
* `GET /api/v1/books/price-range?min={min}&max={max}`: Filtra livros por uma faixa de preço.

**Desafio 1: Sistema de Autenticação**
* **Implementação:** Adicionar autenticação com JWT para proteger rotas sensíveis.
* **Endpoints de Autenticação:**
    * `POST /api/v1/auth/login`: Para obter um token de acesso.
    * `POST /api/v1/auth/refresh`: Para renovar um token existente.
* **Proteção de Rotas:** Proteger endpoints de administração, como um para acionar o scraping (`/api/v1/scraping/trigger`).

**Desafio 2: Pipeline "ML-Ready"**
* **Endpoints para ML:**
    * `GET /api/v1/ml/features`: Retorna dados formatados para serem usados como features em modelos.
    * `GET /api/v1/ml/training-data`: Fornece um dataset pronto para treinamento de modelos.
    * `POST /api/v1/ml/predictions`: Endpoint para receber e possivelmente processar predições de um modelo.

**Desafio 3: Monitoramento & Analytics**
* **Logs:** Implementar logs estruturados para registrar todas as chamadas feitas à API.
* **Métricas:** Coletar métricas de performance da API.
* **Dashboard:** Criar um dashboard simples para visualização de uso da API (recomenda-se o uso do Streamlit).