from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


def ativa():

    # Inicializa o navegador Chrome
    # O driver deve estar na mesma pasta do script ou no PATH do sistema
    driver = webdriver.Chrome()
    driver.get("https://situator.delacroy.com.br/app/manager")
    # Abre a página do Google


    # Encontra a box de texto com usuário e senha.
    search_box = driver.find_element(By.NAME, "userName")
    # Digita usuário na caixa de texto
    search_box.send_keys("gabriel.rodrigues")
    # Digita a senha na caixa de texto
    search_box = driver.find_element(By.NAME, "password")
    search_box.send_keys("7536982014")
    # Tecla Enter para iniciar a pesquisa
    search_box.send_keys(Keys.RETURN)

    try:

        # NA PAGINA PRINCIPAL
        # VAI PARA A PARTE DE CADASTRO - Pessoas
        wait = WebDriverWait(driver, 10)
        botao_pessoas = wait.until(EC.element_to_be_clickable((By.ID, "personTab")))
        botao_pessoas.click()

        # SELECIONA O TIPO - Morador
        seleciona_morador = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.people-filter select"))
        )
        tipo = Select(seleciona_morador)
        tipo.select_by_visible_text("Todos")
        time.sleep(1)

        while True:
            try:
                # SELECIONA O NOME DA PESSOA E ABRE O REGISTRO
                print("Qual o CPF da pessoa que deseja ativar o acesso?")
                cpf = input() # 15422910702  18599453840
                while True:
                    if not validar_cpf(cpf):
                        cpf = input("CPF invalido, digite novamente: ")
                    elif not cpf.isdigit():
                        cpf = input("CPF invalido, digite novamente: ")
                    else:
                        break


                # SELECIONA O PACIENTE PELO CPF
                campo_documento = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[ng-model='pagination.filters.document']"))
                )
                # 2. Envia o Cpf do paciente
                campo_documento.send_keys(cpf)
                time.sleep(5)
                campo_documento.clear()
                editar_pessoa = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a[title='Editar pessoa']"))
                )
                editar_pessoa.click()
                # ALTERA O TIPO PARA VISITANTE
                seletor = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='personType']"))
                )
                # 2. Envie o texto da opção desejada diretamente para o elemento.
                seletor.send_keys("Visitante")
                time.sleep(2)
                # ALTERA O PERFIL DE ACESSO PARA `VISITANTES VITRIUM`
                perfil = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='type']"))
                )
                perfil.send_keys("VITRIUM SUB B")

                # CLICA NO BOTÃO DE ATIVO
                checkbox_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "checkAtivo"))
                )

                # Use JavaScript para executar o clique
                driver.execute_script("arguments[0].click();", checkbox_input)
                time.sleep(2)

                # MUDA PARA A PARTE 4
                salve_clone = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='4']"))
                )
                salve_clone.click()

                # ALTERA A PERMISSÃO DE ACESSO
                # 1. Encontre o elemento <select> pelo seu atributo 'ng-model'
                seletor_permissao = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "select[ng-model='wizard.person.accessPermission']"))
                )

                # 2. Envie o texto da opção desejada ("Autorizado") diretamente para o elemento
                seletor_permissao.send_keys("Autorizado")

                # MUDA PARA A PARTE 6 E SALVA
                salve_clone = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='6']"))
                )
                salve_clone.click()
                salve = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.NAME, "save"))
                )
                salve.click()
                time.sleep(1)
            except TimeoutException:
                campo_documento.clear()

                continue
    finally:
        # Fecha o navegador
        driver.quit()


def validar_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = ''.join([c for c in cpf if c.isdigit()])

    # Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    # Verifica se o CPF não é uma sequência de números repetidos (ex: 111.111.111-11)
    if cpf == cpf[0] * 11:
        return False

    # Função para calcular os dois dígitos verificadores
    def calcular_digitos(cpf, peso):
        soma = sum(int(cpf[i]) * peso[i] for i in range(len(cpf)))
        resto = soma % 11
        if resto < 2:
            return 0
        else:
            return 11 - resto

    # Calculando o primeiro dígito verificador
    peso_1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    digito_1 = calcular_digitos(cpf[:9], peso_1)

    # Calculando o segundo dígito verificador
    peso_2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    digito_2 = calcular_digitos(cpf[:10], peso_2)

    # Verifica se os dígitos verificadores calculados são iguais aos fornecidos
    return cpf[-2:] == f"{digito_1}{digito_2}"


# Executa o programa
if __name__ == "__main__":
    ativa()