from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from IPython.display import display
import unittest


#criando navegador
nav = webdriver.Chrome()

#importar/visualizar base de dados
tabela_produtos = pd.read_excel("buscas.xlsx")
display(tabela_produtos)

#entrar no google
nav.get("https://www.google.com/")

produto = 'iphone 12 64gb'
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
    preco = resultado.find_elements(By.CLASS_NAME, 'T14wmb').text
    nome = resultado.find_elements(By.CLASS_NAME, 'Xjkr3b').text
    link = resultado.find_elements(By.CLASS_NAME, 'shntl').text
    print(preco, nome, link)

#para cada item na base de dados ->
    #procurar produto no google shopping
        #verificar se algum produto está na faixa de preço
    #procurar produto no buscape
        #verificar se algum produto está na faixa de preço
#salvar as ofertas no dataframe(tabela)
#exportar p excel
#enviar para o e-mail o resultado da tabela

