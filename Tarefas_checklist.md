Claro, aqui está um checklist simplificado em formato Markdown para você acompanhar o progresso do seu projeto.

### Checklist do Tech Challenge

**Fase 1: Coleta de Dados**
- [x] Criar script de web scraping para o site `https://books.toscrape.com/`.
- [x] Extrair todos os livros e seus dados (título, preço, avaliação, etc.).
- [x] Salvar os dados coletados em um arquivo CSV.
- [ ] Documentar o script de scraping.

**Fase 2: Desenvolvimento da API**
- [x] Escolher a tecnologia da API (Flask ou FastAPI).
- [x] Implementar o endpoint `GET /api/v1/health`.
- [x] Implementar o endpoint `GET /api/v1/books`.
- [x] Implementar o endpoint `GET /api/v1/books/{id}`.
- [x] Implementar o endpoint `GET /api/v1/books/search`.
- [x] Implementar o endpoint `GET /api/v1/categories`.
- [x] Documentar a API com Swagger (ou similar).

**Fase 3: Deploy e Documentação**
- [ ] Organizar o código em um repositório no GitHub.
- [ ] Escrever um `README.md` completo com todas as seções necessárias.
- [ ] Fazer o deploy da API em uma plataforma pública (Heroku, Render, etc.).
- [ ] Garantir que o link de deploy esteja funcional.
- [ ] Criar o plano arquitetural do projeto.

**Fase 4: Apresentação e Extras**
- [ ] Gravar o vídeo de apresentação (3-12 minutos).
- [ ] Realizar os cursos de IA Generativa do Google Cloud.
- [ ] Enviar o comprovante de conclusão dos cursos.

---

### Desafios Adicionais (Bônus)

- [ ] **Endpoints de Insights:**
    - [ ] `GET /api/v1/stats/overview`
    - [ ] `GET /api/v1/stats/categories`
    - [ ] `GET /api/v1/books/top-rated`
    - [ ] `GET /api/v1/books/price-range`
- [ ] **Sistema de Autenticação:**
    - [ ] Implementar autenticação com JWT.
    - [ ] Criar endpoints `POST /api/v1/auth/login` e `refresh`.
    - [ ] Proteger rotas de administração.
- [ ] **Pipeline ML-Ready:**
    - [ ] Criar endpoint `GET /api/v1/ml/features`.
    - [ ] Criar endpoint `GET /api/v1/ml/training-data`.
    - [ ] Criar endpoint `POST /api/v1/ml/predictions`.
- [ ] **Monitoramento & Analytics:**
    - [ ] Implementar logs estruturados.
    - [ ] Coletar métricas de performance.
    - [ ] Criar um dashboard de visualização (Streamlit).
