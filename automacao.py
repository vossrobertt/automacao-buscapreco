from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from IPython.display import display
import time

# criando navegador
nav = webdriver.Chrome('/Users/robertvoss/Documents/GitHub/automacao-buscapreco/chromedriver')

# importar/visualizar base de dados
tabela_produtos = pd.read_excel("buscas.xlsx")
display(tabela_produtos)


def busca_google_shopping(nav, produto, termos_banidos, preco_minimo,
                          preco_maximo) :  # funcao para pegar produto, termos banidos, precos e nome

    # entrar no google
    nav.get("https://www.google.com/")
    # tratando valores
    produto = produto.lower()
    termos_banidos = termos_banidos.lower()
    lista_termos_banidos = termos_banidos.split(" ")
    lista_termos_produto = produto.split(" ")
    preco_maximo = float(preco_maximo)
    preco_minimo = float(preco_minimo)

    # pesquisar o nome do produto no google
    nav.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(produto)
    nav.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(
        Keys.ENTER)
    # clicar no produto
    elementos = nav.find_elements(By.CLASS_NAME, 'hdtb-mitem')
    for item in elementos:
        if "Shopping" in item.text:
            item.click()
            break
    # pegar o preço do produto
    lista_resultados = nav.find_elements(By.CLASS_NAME, 'sh-dgr__grid-result')
    lista_ofertas = []  # lista que a funcao vai dar como resposta
    for resultado in lista_resultados:
        nome = resultado.find_element(By.CLASS_NAME, 'Xjkr3b').text
        nome = nome.lower()

        # verificacao do nome
        tem_termos_banidos = False
        for palavra in lista_termos_banidos:
            if palavra in nome:
                tem_termos_banidos = True
        #verificar se o nome tem todos os termos do nome do produto
        tem_todos_termos_produto = True
        for palavra in lista_termos_produto:
            if palavra not in nome:
                tem_todos_termos_produto = False

        # se tem_termos_banidos = False e o tem_todos_termos_produto=True entao
        if not tem_termos_banidos and tem_todos_termos_produto:  # verifica nome
            preco = resultado.find_element(By.CLASS_NAME, 'a8Pemb').text
            preco = preco.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
            preco = float(preco)

            # verificando se preco ta minimo ou maximo
            if preco_minimo <= preco <= preco_maximo:
                elemento_link = resultado.find_element(By.CLASS_NAME, 'aULzUe')
                elemento_pai = elemento_link.find_element(By.XPATH, '..')
                link = elemento_pai.get_attribute('href')
                lista_ofertas.append((nome, preco, link))

    return lista_ofertas


def busca_buscape(nav, produto, termos_banidos, preco_minimo, preco_maximo) :
    # tratar valores da funçao
    preco_maximo = float(preco_maximo)
    preco_minimo = float(preco_minimo)
    produto = produto.lower()
    termos_banidos = termos_banidos.lower()
    lista_termos_banidos = termos_banidos.split(" ")
    lista_termos_produto = produto.split(" ")

    # entrar no buscape
    nav.get("https://www.buscape.com.br")
    # pesquisar pelo produto no buscape
    nav.find_element(By.CLASS_NAME, 'AutoCompleteStyle_textBox__eLv3V').send_keys(produto, Keys.ENTER)
    # pegar a lista de resultados da busca do buscape
    time.sleep(5)
    lista_resultados = nav.find_elements(By.CLASS_NAME, 'Cell_Content__fT5st')
    # para cada resultado
    lista_ofertas = [] #lista q vai dar a funcao como resposta
    for resultado in lista_resultados :
        preco = resultado.find_element(By.CLASS_NAME, 'CellPrice_MainValue__JXsj_').text
        nome = resultado.get_attribute('title')
        nome = nome.lower()
        link = resultado.get_attribute('href')

    # ver se ele tem algum termo banido
        tem_termos_banidos = False
        for palavra in lista_termos_banidos:
            if palavra in nome:
                tem_termos_banidos = True
    # ver se ele tem todos os termos do nosso produto

        tem_todos_termos_produto = True
        for palavra in lista_termos_produto:
            if palavra not in nome:
                tem_todos_termos_produto = False

        if not tem_termos_banidos and tem_todos_termos_produto:
            preco = preco.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
            preco = float(preco)
            if preco_minimo <= preco <= preco_maximo:
                lista_ofertas.append((nome, preco, link))

    return lista_ofertas
    # ver se o preço esta na faixa de preço ideal

    # retornar lista de ofertas

for linha in tabela_produtos.index:
produto = 'iphone 12 64 gb'
termos_banidos = 'mini watch'
preco_minimo = '3000'
preco_maximo = '6000'

lista_ofertas_buscape = busca_buscape(nav, produto, termos_banidos, preco_minimo, preco_maximo)
print(lista_ofertas_buscape)
# lista_ofertas_google_shopping = busca_google_shopping(nav, produto, termos_banidos, preco_minimo, preco_maximo)
# print(lista_ofertas_google_shopping)

# exportar p excel


# enviar para o e-mail o resultado da tabela
