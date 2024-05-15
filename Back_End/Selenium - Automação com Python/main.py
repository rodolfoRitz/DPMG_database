#python -m venv env, cd env, \Scripts\activate, Set-ExecutionPolicy Unrestricted -Force (caso de erro), Set-ExecutionPolicy  -Scope CurrentUser  -ExecutionPolicy RemoteSigned

# pip install selenium, pip install webdriver
# pytest, trio, pytest-trio, flake8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import pyautogui # Fornece métodos para controlar mouse e teclado.

from cpf import *
from nome import *
from nascimento import *
import time
import random

nav = webdriver.Chrome() # Utiliza o navegador Chrome
wait = WebDriverWait(nav, 12)

nom = nome.gerar_nome_aleatorio
nac = nascimento.gerar_data_nascimento_aleatoria

nav.get("https://tst.gerais.mg.def.br/sistemas/scsdp/") # Entra nesse site
time.sleep(2)

nav.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[2]/div/div[1]/div/div[2]').click() # Login
time.sleep(0.5)
nav.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[2]/div/div[3]/form/div/label[1]/div/div[1]/div[2]/input').send_keys("08515583640")
time.sleep(2)
nav.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[2]/div/div[3]/form/div/label[2]/div/div[1]/div[2]/input').send_keys("Def@2023")
time.sleep(2)
nav.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[2]/div/div[3]/form/div/div/div[1]/div/button').click() # Entra no DPMG
wait.until(EC.url_to_be('https://tst.gerais.mg.def.br/sistemas/gerais/'))
time.sleep(1)

#nav.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[2]/div/div[3]/form/div/div/div[1]/div/button').click() 
nav.find_element(By.XPATH, '/html/body/div[1]/div/header/div[1]/button[1]').click() # Entra na aba lateral
time.sleep(1)
nav.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/nav/ul/li[10]/i').click() # Entra no 'Servidor'
time.sleep(2)
nav.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/div/div/div/div/div/div/div/div[2]/div[1]/div/div[2]').click() # Entra em Atendimento
time.sleep(2)

# MUDAR DE FRAME
#nav.switch_to.frame(By.XPATH, '/html/body/div[1]/div/div/main')
nav.switch_to.frame('dpmg-frame-gerais')

nav.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[1]/div/div[1]/div[2]/button').click() # NOVO
time.sleep(2)
nav.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div/form/div[1]/div/div[2]/div[2]/div[3]/button[1]').click() # CADASTRO
time.sleep(2)
nav.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div/form/div[1]/div[1]/label/div/div[1]/div[1]/input').send_keys(f"{nom}") # nome_gerado
time.sleep(2)
nav.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div/form/div[1]/div[2]/label/div/div[1]/div/input').send_keys(f"{nom}")
time.sleep(2)
nav.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div/form/div[1]/div[3]/label/div/div[1]/div/input').send_keys(f"{nac}")
time.sleep(2)
nav.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div/form/div[4]/div/form/div/div[2]/div[1]/div[1]/label/div/div[1]/div/input').send_keys(f"{nac}")
time.sleep(2)
nav.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div/form/div[4]/div/form/div/div[2]/div[1]/div[1]/label/div/div[1]/div/input').send_keys(f"{nom}") #Filiação
time.sleep(2)
nav.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div/div[1]/div/div[2]/div[2]/div[2]/div/div[2]/div/div/div/div/form/div[4]/div/form/div/div[2]/div[1]/div[2]/label/div/div[1]/div[2]').click()

for i in range(50):
    
    pass

input()
nav.quit()

'''
# Wait for the element to be clickable (change timeout and adjust conditions as needed)
wait = WebDriverWait(nav, 10)
element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/header/div[1]/button[1]')))

# Once the element is found, perform the click
element.click()
'''

...

'''
title = nav.title

nav.implicitly_wait(0.5)

text_box = nav.find_element(by=By.NAME, value="my-text")
submit_button = nav.find_element(by=By.CSS_SELECTOR, value="button")

text_box.send_keys("Selenium")
submit_button.click()

text = message.text

nav.quit()
'''
'''
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://www.selenium.dev/selenium/web/web-form.html")

title = driver.title

driver.implicitly_wait(0.5)

text_box = driver.find_element(by=By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

text_box.send_keys("Selenium")
submit_button.click()

message = driver.find_element(by=By.ID, value="message")
text = message.text

driver.quit()
'''

'''
def test_pauses(driver):
    driver.get('https://selenium.dev/selenium/web/mouse_interaction.html')

    start = time()

    clickable = driver.find_element(By.ID, "clickable")
    ActionChains(driver)\
        .move_to_element(clickable)\
        .pause(1)\
        .click_and_hold()\
        .pause(1)\
        .send_keys("abc")\
        .perform()

    duration = time() - start
    assert duration > 2
    assert duration < 3


def test_releases_all(driver):
    driver.get('https://selenium.dev/selenium/web/mouse_interaction.html')

    clickable = driver.find_element(By.ID, "clickable")
    ActionChains(driver)\
        .click_and_hold(clickable)\
        .key_down(Keys.SHIFT)\
        .key_down("a")\
        .perform()

    ActionBuilder(driver).clear_actions()

    ActionChains(driver).key_down('a').perform()

    assert clickable.get_attribute('value')[0] == "A"
    assert clickable.get_attribute('value')[1] == "a"
    '''