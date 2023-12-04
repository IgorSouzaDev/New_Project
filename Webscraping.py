from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from time import sleep

options = webdriver.FirefoxOptions()

#options.add_argument("--headless")
driver = webdriver.Firefox(options=options)


wait = WebDriverWait(driver, timeout=2)


driver.get('https://www.supermercadosbh.com.br/receitas/')

def sereach_prod():
    list_receitas = []
    receitas = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/section[2]/div/div[3]/div')))
    list_receitas.append(receitas.text)
    return list_receitas

def limpar_lista(list_receitas):
    # Separa a lista pelos epaços
    itens = list_receitas[0].splitlines()
    # Retira os espaços da lista
    lista_limpa = [item.strip() for item in itens if item.strip()]
    return lista_limpa


lista_subtitulo=[]
lista_ingrediente=[]




def get_data(list_receitas):
    recipes_list = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'recipes-list')))
    recipe_links = recipes_list.find_elements(By.TAG_NAME, 'a')

    for link in recipe_links:
        # Obtém a URL do link
        url = link.get_attribute('href')
        print("acessando links {}".format(url))
        # Abre o link em uma nova aba
        driver.execute_script("window.open('{}', '_blank');".format(url))

        # Muda para a nova aba
        driver.switch_to.window(driver.window_handles[-1])

        try:
            # Espera pelo subtitulo
            sub_titulo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.page-subtitle-text:nth-child(1)')))
            lista_subtitulo.append(sub_titulo.text)

            # Espera pelos ingredientes
            ingrediente = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.recipes-post')))
            lista_ingrediente.append(ingrediente.text)

        except Exception as e:
            print(f"Erro ao extrair informações: {e}")

        finally:
            # Fecha a aba atual
            driver.close()

            # Volta para a aba principal
            driver.switch_to.window(driver.window_handles[0])






# Chamando as funções
lista_receitas = sereach_prod()
lista_limpa = limpar_lista(lista_receitas)
get_data(lista_limpa)



print(lista_subtitulo)
#print(lista_ingrediente)




#driver.quit()


