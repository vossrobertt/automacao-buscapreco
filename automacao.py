from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from IPython.display import display


#criando navegador
nav = webdriver.Chrome('/Users/robertvoss/Documents/GitHub/automacao-buscapreco/chromedriver')

#importar/visualizar base de dados
tabela_produtos = pd.read_excel("buscas.xlsx")
display(tabela_produtos)

#entrar no google
nav.get("https://www.google.com/")

produto = 'iphone 12 64 gb'
produto = produto.lower()

termos_banidos = 'mini watch'
termos_banidos = termos_banidos.lower()
lista_termos_banidos = termos_banidos.split(" ")
lista_termos_produto = produto.split(" ")
preco_minimo = '3000'
preco_maximo = '3500'
#pesquisar o nome do produto no google
nav.find_element(By.XPATH,'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(produto)
nav.find_element(By.XPATH,'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
#clicar no produto
elementos = nav.find_elements(By.CLASS_NAME,'hdtb-mitem')
for item in elementos:
    if "Shopping" in item.text:
        item.click()
        break
#pegar o preço do produto
lista_resultados = nav.find_elements(By.CLASS_NAME, 'sh-dgr__grid-result')

for resultado in lista_resultados:
    nome = resultado.find_element(By.CLASS_NAME, 'Xjkr3b').text
    nome = nome.lower()

    #verificacao do nome
    tem_termos_banidos = False
    for palavra in lista_termos_banidos:
        if palavra in nome:
            tem_termos_banidos = True

    tem_todos_termos_produto = True
    for palavra in lista_termos_produto:
        if palavra not in nome:
            tem_todos_termos_produto = False

    # se tem_termos_banidos = False e o tem_todos_termos_produto=True entao
    if not tem_termos_banidos and tem_todos_termos_produto: #verifica nome
        preco = resultado.find_element(By.CLASS_NAME, 'a8Pemb').text
        preco = preco.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
        preco = float(preco)

    # verificando se preco ta minimo ou maximo
        preco_maximo = float(preco_maximo)
        preco_minimo = float(preco_minimo)
        if preco_minimo <= preco <= preco_maximo:
            elemento_link = resultado.find_element(By.CLASS_NAME, 'aULzUe')
            elemento_pai = elemento_link.find_element(By.XPATH, '..')
            link = elemento_pai.get_attribute('href')
            print(preco, nome, link)





#para cada item na base de dados ->
    #procurar produto no google shopping
        #verificar se algum produto está na faixa de preço
    #procurar produto no buscape
        #verificar se algum produto está na faixa de preço
#salvar as ofertas no dataframe(tabela)
#exportar p excel
#enviar para o e-mail o resultado da tabela

