from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


def automacao_remove():
    """
    Automatiza uma pesquisa no Google, digitando na caixa de texto
    e clicando no botão de pesquisa.
    """
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
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.form-group select"))
        )
        tipo = Select(seleciona_morador)
        tipo.select_by_visible_text("Morador")

        # SELECIONA A UNIDADE E PESQUISA PELA SALA
        unidade = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.people-filter input"))
        )
        unidade.send_keys("0210")

        while True:
            try:
                # SELECIONA O NOME DA PESSOA E ABRE O REGISTRO
                print("Qual o nome da pessoa que deseja transformar em visitante?")
                procurar_pessoa = input().upper()

                nome_paciente = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.form-group input"))

                )
                nome_paciente.send_keys(procurar_pessoa)

                # BOTÃO DE EDITAR PESSOA
                xpath_do_botao = "//tr[./td[text()='" + procurar_pessoa + "']]//a[@title='Editar pessoa']"
                wait = WebDriverWait(driver, 10)
                botao_editar = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_do_botao)))
                botao_editar.click()
                time.sleep(2)
                nome_paciente.clear()
                # SELECIONA O TIPO MORADOR E ALTERA PARA VISITANTE
                seletor = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='personType']"))
                )
                seletor.send_keys("Visitante")

                # ALTERA O PERFIL DE ACESSO PARA `VISITANTES VITRIUM`
                perfil = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='type']"))
                )
                perfil.send_keys("VISITANTES VITRIUM")
                time.sleep(2)

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
            except TimeoutException:  # Sintaxe correta
                # Este código SÓ executa se o 'wait.until' falhar
                print(f"AVISO: Paciente '{procurar_pessoa}' não encontrado na lista.")
                print("Reiniciando para a próxima busca...")
                nome_paciente.clear()
                continue
    finally:
        # Fecha o navegador
        driver.quit()


# Executa o programa
if __name__ == "__main__":
    automacao_remove()