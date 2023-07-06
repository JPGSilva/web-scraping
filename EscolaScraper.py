import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class EscolaScraper:
    def __init__(self, nome, endereco, cidade, estado, telefone, cep, nivel_escolaridade):
        self.nome = nome
        self.endereco = endereco
        self.cidade = cidade
        self.estado = estado
        self.telefone = telefone
        self.cep = cep
        self.nivel_escolaridade = nivel_escolaridade


def coletar_escolas():
    escolas = []


    service = Service('/Users/joaosilva/Downloads/chromedriver_mac64/chromedriver')  # Substitua pelo caminho do chromedriver
    options = Options()
    options.add_argument('--headless')  # Executar o Chrome em modo headless (sem interface gráfica)
    driver = webdriver.Chrome(service=service, options=options)


    driver.get('https://www.google.com')
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys('escolas de tres lagoas')
    search_box.send_keys(Keys.RETURN)

    resultados = driver.find_elements(By.CLASS_NAME, 'g')

    for resultado in resultados:
        try:
            nome = resultado.find_element(By.TAG_NAME, 'h3').text
            endereco = resultado.find_element(By.CSS_SELECTOR, 'div.VkpGBb').text
            cidade_estado = resultado.find_element(By.CSS_SELECTOR, 'span.B6fmyf').text
            telefone = resultado.find_element(By.CSS_SELECTOR, 'div.xpdopen > div > div > div > span').text
            cep = resultado.find_element(By.CSS_SELECTOR, 'span.LrzXr').get_attribute('data-attrid')
            nivel_escolaridade = resultado.find_element(By.CSS_SELECTOR, 'div.qsm0tb').text

            cidade_estado_split = cidade_estado.split(',')
            cidade = cidade_estado_split[0].strip()
            estado = cidade_estado_split[1].strip()

            escola = EscolaScraper(nome, endereco, cidade, estado, telefone, cep, nivel_escolaridade)
            escolas.append(escola)
        except Exception as e:
            print(f"Erro ao extrair informações: {str(e)}")

    driver.quit()

    return escolas


def salvar_csv(escolas):
    with open('escolas.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Endereço', 'Cidade', 'Estado', 'Telefone', 'CEP', 'Nível de Escolaridade'])
        for escola in escolas:
            writer.writerow([escola.nome, escola.endereco, escola.cidade, escola.estado, escola.telefone,
                             escola.cep, escola.nivel_escolaridade])


escolas = coletar_escolas()
salvar_csv(escolas)