import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager


def coleta_quantidade_paginas(driver:webdriver):
    """
    Coleta a quantidade total de páginas no site principal.

    Args:
        driver (webdriver): Instância do navegador Selenium.

    Returns:
        int: Número total de páginas.
    """

    url = 'https://books.toscrape.com/'
    driver.get(url)
    paginacao = driver.find_element(By.CLASS_NAME, 'current').text
    total_paginas = paginacao.split(' ')[-1]
    return int(total_paginas)

def coleta_links_livros(driver:webdriver, total_paginas:int):
    """
    Percorre todas as páginas do site e coleta os links individuais de cada livro.

    Args:
        driver (webdriver): Instância do navegador Selenium.
        total_paginas (int): Total de páginas no site.

    Returns:
        list[str]: Lista de URLs dos livros.
    """

    links_livros = []
    for pagina in range(1, total_paginas+1):
        url = f'https://books.toscrape.com/catalogue/page-{pagina}.html'
        driver.get(url)
        containers_livros = driver.find_elements(By.CLASS_NAME, 'product_pod')
        for container in containers_livros:
            link_livro = container.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').get_attribute('href')
            links_livros.append(link_livro)
    return links_livros

def coleta_info_livros(driver:webdriver, links_livros:list[str]):
    """
    Visita cada página de livro individual e coleta informações como título, preço, 
    avaliacao, disponibilidade, estoque, categoria e url da imagem.

    Args:
        driver (webdriver): Instância do navegador Selenium.
        links_livros (list[str]): Lista de URLs de cada livro.

    Returns:
        dict: Dicionário com listas de dados para cada campo dos livros.
    """

    info_livros = {
        'titulo': [],
        'preco': [],
        'avaliacao': [],
        'disponibilidade': [],
        'estoque': [],
        'categoria': [],
        'imagem': []
    }
    
    avaliacoes_numericas = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
    }

    for link_livro in links_livros:
        driver.get(link_livro)
        
        info_livros['titulo'].append(driver.find_element(By.CLASS_NAME, 'product_main').find_element(By.TAG_NAME, 'h1').text)
        info_livros['preco'].append(driver.find_element(By.CLASS_NAME, 'price_color').text.replace('£', '').strip())
        info_livros['avaliacao'].append(avaliacoes_numericas.get(driver.find_element(By.CLASS_NAME, 'star-rating').get_attribute('class').split()[-1]))
        info_livros['disponibilidade'].append(driver.find_element(By.CLASS_NAME, 'instock').text.split('(')[0].strip())
        info_livros['estoque'].append(driver.find_element(By.CLASS_NAME, 'instock').text.split('(')[1].split(' ')[0])
        info_livros['categoria'].append(driver.find_element(By.CLASS_NAME, 'breadcrumb').text.split(' ')[2]) 
        info_livros['imagem'].append(driver.find_element(By.CLASS_NAME, 'thumbnail').find_element(By.TAG_NAME, 'img').get_attribute('src'))

    return info_livros


# ----------------------- PROGRAMA PRINCIPAL -----------------------
def main ():
    print('🔄 Iniciando o scraper de livros do site Books to Scrape...')
    navegador_visivel = input("Deseja abrir o navegador visivelmente? (s/n): ").strip().lower()

    # Configuração do navegador
    print('🛠️  Configurando o navegador...')
    options = Options()
    if navegador_visivel != 's':
        print("🔒 Modo oculto (headless) ativado.")
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Coleta de dados
    print('🌐 1/4 Encontrando total de páginas...')
    total_paginas = coleta_quantidade_paginas(driver)
    print(f'📄 {total_paginas} páginas encontradas.')

    print('🌐 2/4 Coletando links de todos os livros...')
    links_livros = coleta_links_livros(driver, total_paginas)
    print(f'🔗 {len(links_livros)} links coletados.')

    print('🌐 3/4 Coletando as informações de cada um dos livros...')
    info_livros = coleta_info_livros(driver, links_livros)
    print(f'📘 {len(info_livros["titulo"])} livros processados com sucesso.')

    driver.quit()
    print('🧹 Navegador encerrado.')

    # Salvamento dos dados
    nome_arquivo_csv = input('💾 Escreva um nome para o arquivo de dados (apenas o nome, sem o formato .csv): ')
    print('📂 4/4 Salvando arquivo...')
    tabela_livros = pd.DataFrame(info_livros)
    tabela_livros.to_csv(f'data/{nome_arquivo_csv}.csv', index = False, sep = ';')
    print('✅ Arquivo salvo na pasta /data.')

# main()

def rodar_scraping():
    main()