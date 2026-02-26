import os

from selenium.common import TimeoutException, StaleElementReferenceException, ElementClickInterceptedException, \
    NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from br.com.sistema.ativa.application_ativar import botao_ativacao

def ativa():

    driver = initialize_start()

    try:

        status_filtro = "Inativos"
        sala = "0217"
        tipo = "Visitante"

        page_pessoas(driver, status_filtro, sala, tipo)

        while True:

            # GARANTE QUE A UNIDADE 217 ESTEJA PRESENTE
            nome_sala = "SALA B 0217 - NEFROSTAR, TORRE B"
            if validar_sala_na_lista(driver, nome_sala):
                print("SALA OK")

                editar_pessoa(driver)

                altera_tipo(driver)

                altera_perfil_de_acesso(driver)

                botao_ativacao(driver)

                authorization(driver)

                last_part_save(driver)

                time.sleep(9)

    finally:
        print("")

def authorization(driver):
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

def last_part_save(driver):
    # MUDA PARA A PARTE 6 E SALVA
    salve_clone = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='6']"))
    )
    salve_clone.click()
    salve = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, "save"))
    )
    salve.click()

    # CLICA NO 'X' PARA FECHAR O MODAL FINAL
    botao_fechar_x_final = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "div.close-modal-container a[ng-click='closeModal();']"))
    )
    time.sleep(1)
    botao_fechar_x_final.click()
    print("Finalizado com sucesso!✅")


# SELECIONA O TIPO MORADOR E ALTERA PARA VISITANTE
def altera_tipo(driver):
    time.sleep(1)
    seletor = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='personType']"))
    )
    # 2. Envie o texto da opção desejada diretamente para o elemento.
    seletor.send_keys("Morador")
    time.sleep(1)


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

    # MUDA PARA A PARTE 2
def unidades_associar_unidade(driver):

    muda_para_unidades = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='2']"))
    )
    muda_para_unidades.click()
    time.sleep(1)

    # CLICA EM 'ASSOCIAR UNIDADE'
    botao_associar_unidade = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Associar unidade"))
    )
    botao_associar_unidade.click()
    time.sleep(1)

    # INSERE TEXTO NO CAMPO 'PESQUISAR' DA UNIDADE
    campo_pesquisar_unidade = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[ng-model='filters.search']"))
    )

    local = input("Qual o número da sala? ")

    if local != "0" and local != "":
        campo_pesquisar_unidade.clear()

        for caractere in local:
            campo_pesquisar_unidade.send_keys(caractere)
            time.sleep(0.05)

        time.sleep(1)

        # MARCA O CHECKBOX DA UNIDADE (Alternativa com JS)
        checkbox_unidade = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "checkAtivo0"))
        )
        driver.execute_script("arguments[0].click();", checkbox_unidade)
        time.sleep(1)

        # CLICA NO BOTÃO 'SALVAR' DO MODAL DE UNIDADES
        botao_salvar_modal_unidade = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.button-modal button[type='submit']"))
        )
        botao_salvar_modal_unidade.click()
        time.sleep(1)

    else:
        # CLICA NO 'X' PARA FECHAR O MODAL
        botao_fechar_x_modal = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.close-modal-container a[ng-click='closeClick();']"))
        )
        botao_fechar_x_modal.click()
        time.sleep(1)


# ALTERA O PERFIL DE ACESSO PARA `VITRIUM SUB B`
def altera_perfil_de_acesso(driver):
    time.sleep(1)
    perfil = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='type']"))
    )
    perfil.send_keys("VITRIUM SUB B")
    time.sleep(1)


def validar_sala_na_lista(driver, nome_sala):
    """
    Verifica se uma sala específica está presente na coluna de unidades.
    Retorna True se encontrar, False se não.
    """
    try:
        # O seletor procura: uma div, dentro da tabela, que tenha o title igual à sala
        time.sleep(1)
        seletor = f"td.units-column div[title='{nome_sala}']"

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, seletor))
        )
        return True
    except TimeoutException:
        return False

# CLICK EM EDITAR CADASTRO
def editar_pessoa(driver):
    time.sleep(1)
    editar_pessoa = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[title='Editar pessoa']"))
    )
    editar_pessoa.click()
    time.sleep(1)


def page_pessoas(driver, status_filter, sala, tipo):
    # NA PAGINA PRINCIPAL
    # VAI PARA A PARTE DE CADASTRO - Pessoas
    wait = WebDriverWait(driver, 10)
    botao_pessoas = wait.until(EC.element_to_be_clickable((By.ID, "personTab")))
    botao_pessoas.click()

    # SELECIONA O TIPO - Morador
    seleciona_status = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.people-filter select"))
    )
    status = Select(seleciona_status)
    status.select_by_visible_text(status_filter)
    time.sleep(1)

    # SELECIONA A UNIDADE E PESQUISA PELA SALA
    unidade = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.people-filter input"))
    )
    unidade.send_keys(sala)
    time.sleep(1)

    # SELECIONA O TIPO VISITANTE
    seleciona_tipo = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "select[ng-model='pagination.filters.personType']"))
    )
    select_objeto = Select(seleciona_tipo)
    select_objeto.select_by_visible_text(tipo)
    time.sleep(1)


def initialize_start():
    username = os.getenv('VI_USERNAME')
    password = os.getenv('VI_PASSWORD')

    opcoes = Options()

    time.sleep(1)
    # Inicializa o navegador Chrome
    # O driver deve estar na mesma pasta do script ou no PATH do sistema
    driver = webdriver.Chrome(opcoes)
    driver.maximize_window()

    tamanho_tela = driver.get_window_size()
    largura_total = tamanho_tela['width']
    altura_total = tamanho_tela['height']

    # 3. Define a posição e o tamanho para simular "Win + Esquerda"
    # x=0, y=0 -> Canto superior esquerdo
    # width = metade da largura
    # height = altura total
    driver.set_window_rect(x=0, y=0, width=largura_total // 2, height=altura_total)

    # Abre a página do Google
    driver.get("https://situator.delacroy.com.br/app/manager")

    # Encontra a box de texto com usuário e senha.
    search_box = driver.find_element(By.NAME, "userName")
    # Digita usuário na caixa de texto

    # Digita a senha na caixa de texto
    search_box.send_keys(username)
    search_box = driver.find_element(By.NAME, "password")
    search_box.send_keys(password)
    search_box.send_keys(Keys.RETURN)

    return driver



# Executa o programa
if __name__ == "__main__":
    ativa()
