import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager


def coleta_quantidade_paginas(driver):
    url = 'https://books.toscrape.com/'
    driver.get(url)
    paginacao = driver.find_element(By.CLASS_NAME, 'current').text
    total_paginas = paginacao.split(' ')[-1]
    return total_paginas

def coleta_links_livros(driver, total_paginas):
    links_livros = []
    for pagina in range(1, int(total_paginas)+1):
        url = f'https://books.toscrape.com/catalogue/page-{pagina}.html'
        driver.get(url)
        containers_livros = driver.find_elements(By.CLASS_NAME, 'product_pod')
        for container in containers_livros:
            link_livro = container.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').get_attribute('href')
            links_livros.append(link_livro)
    return links_livros

def coleta_info_livros(driver, links_livros):
    info_livros = {}

    titulo_livros = []
    preco_livros = []
    avaliacao_livros = []
    disponibilidade_livros = []
    estoque_livros = []
    categoria_livros = []
    imagem_livros = []

    for link_livro in links_livros:
        driver.get(link_livro)
        
        titulo_livros.append(driver.find_element(By.CLASS_NAME, 'product_main').find_element(By.TAG_NAME, 'h1').text)
        preco_livros.append(driver.find_element(By.CLASS_NAME, 'price_color').text)
        avaliacao_livros.append(driver.find_element(By.CLASS_NAME, 'star-rating').get_attribute('class').split()[-1])
        disponibilidade_livros.append(driver.find_element(By.CLASS_NAME, 'instock').text.split('(')[0].strip())
        estoque_livros.append(driver.find_element(By.CLASS_NAME, 'instock').text.split('(')[1].split(' ')[0])
        categoria_livros.append(driver.find_element(By.CLASS_NAME, 'breadcrumb').text.split(' ')[2]) 
        imagem_livros.append(driver.find_element(By.CLASS_NAME, 'thumbnail').find_element(By.TAG_NAME, 'img').get_attribute('src'))

    info_livros['titulo'] = titulo_livros
    info_livros['preco'] = preco_livros
    info_livros['avaliacao'] = avaliacao_livros
    info_livros['disponibilidade'] = disponibilidade_livros
    info_livros['estoque'] = estoque_livros
    info_livros['categoria'] = categoria_livros
    info_livros['imagem'] = imagem_livros

    return info_livros


print('🔄 Iniciando o scraper de livros do site Books to Scrape...')
navegador_visivel = input("Deseja abrir o navegador visivelmente? (s/n): ").strip().lower()

print('🛠️  Configurando o navegador...')
options = Options()
if navegador_visivel != 's':
    print("🔒 Modo oculto (headless) ativado.")
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

print('🌐 1/4 Encontrando total de páginas...')
total_paginas = coleta_quantidade_paginas(driver)
print(f'{total_paginas} páginas encontradas.')

print('🌐 2/4 Coletando links de todos os livros...')
links_livros = coleta_links_livros(driver, total_paginas)
print('✅ Coleta dos links dos livros concluída.')

print('🌐 3/4 Coletando as informações de cada um dos livros...')
info_livros = coleta_info_livros(driver, links_livros)
print('✅ Todos os dados foram coletados.')

driver.quit()

nome_arquivo_csv = input('Escreva um nome para o arquivo de dados (apenas o nome, sem o formato .csv): ')
print('🌐 4/4 Salvando arquivo...')
tabela_livros = pd.DataFrame(info_livros)
tabela_livros.to_csv(f'data/{nome_arquivo_csv}.csv', index = False, sep = ';')
print('✅ Arquivo salvo na pasta /data.')